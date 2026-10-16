#!/usr/bin/env python3
"""Shared infrastructure for the armor rework generators.

One cube table drives everything:
  - shelf-packed UV assignment (guaranteed texOffs <-> island match)
  - base + optional emissive 128x128 atlas
  - complete Java EntityModel file (LayerDefinition builder emitted)

Java model contract (layers depend on it):
  - root children: head, body, right_arm, left_arm, right_leg, left_leg
    (+ optional shoulder_left / shoulder_right under body)
  - head/body/arm/leg bones carry PartPose.ZERO; the render layer copyFrom()s
    the parent humanoid model, so positions/rotations come from the player.
  - setPieces(head, chest, legs, feet) toggles per-piece visibility.
"""
import json
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
A = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'opusvsexe')
CLIENT = os.path.join(ROOT, 'src', 'client', 'java')


def java_path(package, cls):
    return os.path.join(CLIENT, *package.split('.'), cls + '.java')


def h01(*args):
    h = 2166136261
    for a in args:
        if isinstance(a, str):
            a = sum(ord(ch) * (i + 7) for i, ch in enumerate(a))
        h ^= (int(a) * 2654435761) & 0xFFFFFFFF
        h = (h * 16777619) & 0xFFFFFFFF
        h ^= h >> 13
    return (h & 0xFFFFFF) / 0xFFFFFF


def c01(v):
    return max(0, min(255, int(round(v))))


def mixc(c1, c2, t):
    return (c01(c1[0] + (c2[0] - c1[0]) * t), c01(c1[1] + (c2[1] - c1[1]) * t),
            c01(c1[2] + (c2[2] - c1[2]) * t), 255)


def shadec(c, f):
    return (c01(c[0] * f), c01(c[1] * f), c01(c[2] * f), 255)


def vnoise(x, y, seed, scale=3):
    gx, gy = math.floor(x / scale), math.floor(y / scale)
    fx, fy = (x / scale) - gx, (y / scale) - gy
    a, b = h01(gx, gy, seed), h01(gx + 1, gy, seed)
    c, d = h01(gx, gy + 1, seed), h01(gx + 1, gy + 1, seed)
    sx = fx * fx * (3 - 2 * fx)
    sy = fy * fy * (3 - 2 * fy)
    top = a + (b - a) * sx
    bot = c + (d - c) * sx
    return top + (bot - top) * sy


# ------------------------------------------------------------------ cube table
class CubeSet:
    def __init__(self, atlas=128):
        self.cubes = []          # dicts: bone, name, o, s, paint, inflate, rot, emissive
        self.atlas = atlas
        self.bone_poses = {}     # bone path (a/b) -> PartPose java string

    def bone(self, path, pose='PartPose.ZERO'):
        self.bone_poses[path] = pose
        return path

    def add(self, bone, name, o, s, paint, inflate=0.0, rot=None, emissive=None):
        self.cubes.append(dict(bone=bone, name=name, o=list(o), s=list(s),
                               paint=paint, inflate=inflate, rot=rot, emissive=emissive))
        return self.cubes[-1]

    def pack(self):
        """Assign texOffs (u, v) per cube. 'uv' may be preset to share an island."""
        def footprint(c):
            w, h, d = (max(1, int(math.floor(v))) for v in c['s'])
            return 2 * (w + d), d + h

        todo = [c for c in self.cubes if 'uv' not in c]
        todo.sort(key=lambda c: (-footprint(c)[1], -footprint(c)[0]))
        x = y = row_h = 0
        for c in todo:
            fw, fh = footprint(c)
            if x + fw > self.atlas:
                x = 0
                y += row_h + 1
                row_h = 0
            if x + fw > self.atlas or y + fh > self.atlas:
                raise RuntimeError(f"UV atlas overflow for {c['name']} ({fw}x{fh}) at ({x},{y})")
            c['uv'] = (x, y)
            x += fw + 1
            row_h = max(row_h, fh)
        return self

    # ---------------- texture ----------------
    def paint_atlas(self, palette):
        """Returns (base_img, emissive_img) as pixel buffers."""
        from PIL import Image
        img = Image.new('RGBA', (self.atlas, self.atlas), (0, 0, 0, 0))
        emi = Image.new('RGBA', (self.atlas, self.atlas), (0, 0, 0, 0))
        px, ex = img.load(), emi.load()
        for c in self.cubes:
            u, v = c['uv']
            w, h, d = (max(1, int(math.floor(x))) for x in c['s'])
            faces = {
                'up':    (u + d, v, w, d),
                'down':  (u + d + w, v, w, d),
                'east':  (u, v + d, d, h),
                'north': (u + d, v + d, w, h),
                'west':  (u + d + w, v + d, d, h),
                'south': (u + d + w + d, v + d, w, h),
            }
            for face, (fx, fy, fw, fh) in faces.items():
                for yy in range(fh):
                    for xx in range(fw):
                        col = c['paint'](xx, yy, fw, fh, face, c['name'])
                        if col is None:
                            continue
                        X, Y = fx + xx, fy + yy
                        if 0 <= X < self.atlas and 0 <= Y < self.atlas:
                            px[X, Y] = col
            if c.get('emissive') is not None:
                u, v = c['uv']
                w, h, d = (max(1, int(math.floor(x))) for x in c['s'])
                faces = {
                    'up': (u + d, v, w, d), 'down': (u + d + w, v, w, d),
                    'east': (u, v + d, d, h), 'north': (u + d, v + d, w, h),
                    'west': (u + d + w, v + d, d, h), 'south': (u + d + w + d, v + d, w, h),
                }
                for face, (fx, fy, fw, fh) in faces.items():
                    for yy in range(fh):
                        for xx in range(fw):
                            col = c['emissive'](xx, yy, fw, fh, face, c['name'])
                            if col is not None:
                                X, Y = fx + xx, fy + yy
                                if 0 <= X < self.atlas and 0 <= Y < self.atlas:
                                    ex[X, Y] = col
        return img, emi

    # ---------------- java ----------------
    def emit_java(self, package, class_name, layer_id, out_path, doc):
        """Write the complete model class with standard piece-visibility contract."""
        bones = {}
        for c in self.cubes:
            bones.setdefault(c['bone'], []).append(c)
        order = list(bones.keys())

        L = []
        w = L.append
        w(f'package {package};')
        w('')
        for imp in ('com.mojang.blaze3d.vertex.PoseStack', 'com.mojang.blaze3d.vertex.VertexConsumer',
                    'net.minecraft.client.model.EntityModel', 'net.minecraft.client.model.geom.ModelLayerLocation',
                    'net.minecraft.client.model.geom.ModelPart', 'net.minecraft.client.model.geom.PartPose',
                    'net.minecraft.client.model.geom.builders.CubeDeformation', 'net.minecraft.client.model.geom.builders.CubeListBuilder',
                    'net.minecraft.client.model.geom.builders.LayerDefinition', 'net.minecraft.client.model.geom.builders.MeshDefinition',
                    'net.minecraft.client.model.geom.builders.PartDefinition', 'net.minecraft.resources.ResourceLocation',
                    'net.minecraft.world.entity.LivingEntity'):
            w(f'import {imp};')
        w('')
        w('/**')
        for dl in doc:
            w(f' * {dl}'.rstrip())
        w(' */')
        w(f'public final class {class_name}<T extends LivingEntity> extends EntityModel<T> {{')
        w('    public static final ModelLayerLocation LAYER_LOCATION =')
        w(f'        new ModelLayerLocation(new ResourceLocation("opusvsexe", "{layer_id}"), "main");')
        w('')
        w('    private final ModelPart root;')
        w(f'    public {class_name}(ModelPart root) {{ this.root = root; }}')
        w('    public ModelPart root() { return root; }')
        for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg'):
            if b in bones:
                getter = {'right_arm': 'rightArm', 'left_arm': 'leftArm',
                          'right_leg': 'rightLeg', 'left_leg': 'leftLeg'}.get(b, b)
                w(f'    public ModelPart {getter}() {{ return root.getChild("{b}"); }}')
        for b in ('shoulder_left', 'shoulder_right'):
            if b in bones:
                getter = 'shoulderLeft' if b == 'shoulder_left' else 'shoulderRight'
                w(f'    public ModelPart {getter}() {{ return root.getChild("body").getChild("{b}"); }}')
        for b in bones:
            if '/' in b and b.count('/') == 1:
                parent, name = b.split('/')
                w(f'    public ModelPart {name}() {{ return root.getChild("{parent}").getChild("{name}"); }}')
        w('')
        w('    /** Per-piece visibility: helmet / cuirass+arms / leggings group / boots group. */')
        w('    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet) {')
        for b in order:
            if b == 'head':
                w('        head().visible = head;')
            elif b in ('body', 'right_arm', 'left_arm', 'shoulder_left', 'shoulder_right'):
                if b == 'body':
                    w('        body().visible = chest;')
                else:
                    getter = {'right_arm': 'rightArm', 'left_arm': 'leftArm',
                              'shoulder_left': 'shoulderLeft', 'shoulder_right': 'shoulderRight'}[b]
                    w(f'        {getter}().visible = chest;')
            elif b in ('right_leg', 'left_leg'):
                leg_getter = 'rightLeg' if b == 'right_leg' else 'leftLeg'
                for c in bones[b]:
                    n = c['name']
                    if any(k in n for k in ('thigh', 'hip', 'pteru')):
                        w(f'        {leg_getter}().getChild("{n}").visible = legs;')
                    elif any(k in n for k in ('boot', 'greave', 'vent', 'sole', 'sandal', 'toe')):
                        w(f'        {leg_getter}().getChild("{n}").visible = feet;')
                    else:
                        w(f'        {leg_getter}().getChild("{n}").visible = legs || feet;')
            elif '/robe_' in b or '/pteruges_' in b:
                w(f'        body().getChild("{b.rsplit("/", 1)[1]}").visible = chest || legs;')
            elif b in ('effects', 'halo'):
                pass  # static decoration, always rendered with its parent piece
        w('    }')
        w('')
        w('    public static LayerDefinition createLayerDefinition() {')
        w('        MeshDefinition mesh = new MeshDefinition();')
        w('        PartDefinition root = mesh.getRoot();')
        # declare standard root bones (those without an explicit parent path)
        root_bones = [b for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg')
                      if b in self.bone_poses or b in bones]
        for b in root_bones:
            pose = self.bone_poses.get(b, 'PartPose.ZERO')
            w(f'        PartDefinition {b} = root.addOrReplaceChild("{b}", CubeListBuilder.create(), {pose});')
        if 'shoulder_left' in bones and 'body' in (bones.keys() | self.bone_poses.keys()):
            w('        PartDefinition shoulder_left = body.addOrReplaceChild("shoulder_left", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));')
            w('        PartDefinition shoulder_right = body.addOrReplaceChild("shoulder_right", CubeListBuilder.create(), PartPose.offset(-5.0F, 2.0F, 0.0F));')
        # declare child bones (paths with '/'), deepest-last order by depth then insertion
        child_bones = [p for p in list(self.bone_poses.keys()) + [c['bone'] for c in self.cubes]
                       if '/' in p]
        seen = []
        for pth in child_bones:
            if pth not in seen:
                seen.append(pth)
        seen.sort(key=lambda p: p.count('/'))
        for pth in seen:
            parent, name = pth.rsplit('/', 1)
            parent_var = parent.rsplit('/', 1)[-1]
            pose = self.bone_poses.get(pth, 'PartPose.ZERO')
            w(f'        PartDefinition {name} = {parent_var}.addOrReplaceChild("{name}", CubeListBuilder.create(), {pose});')
        w('')
        for c in self.cubes:
            u, v = c['uv']
            cw, ch, cd = (max(1, int(math.floor(x))) for x in c['s'])
            x, y, z = c['o']
            inflate = c.get('inflate', 0)
            defstr = f', new CubeDeformation({inflate}f)' if inflate else ''
            bpath = c['bone']
            if bpath in ('shoulder_left', 'shoulder_right'):
                target = bpath
            else:
                target = bpath.rsplit('/', 1)[-1]
            rot = c.get('rot')
            # each cube is a child bone holding exactly one box:
            # - plain: bone at the box corner, box starts at (0,0,0)
            # - rotated: bone at the box CENTER, box centered on origin
            if rot:
                pose = (f'PartPose.offsetAndRotation({x + cw / 2}F, {y + ch / 2}F, {z + cd / 2}F,'
                        f' {rot[0]}F, {rot[1]}F, {rot[2]}F)')
                bx, by, bz = -cw / 2, -ch / 2, -cd / 2
            else:
                pose = f'PartPose.offset({x}F, {y}F, {z}F)'
                bx, by, bz = 0, 0, 0
            w(f'        {target}.addOrReplaceChild("{c["name"]}", CubeListBuilder.create()')
            w(f'            .texOffs({u}, {v}).addBox({bx}F, {by}F, {bz}F, {cw}F, {ch}F, {cd}F{defstr}),')
            w(f'            {pose});')
        w('')
        w(f'        return LayerDefinition.create(mesh, {self.atlas}, {self.atlas});')
        w('    }')
        w('')
        w('    @Override')
        w('    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks,')
        w('                          float netHeadYaw, float headPitch) {')
        w('    }')
        w('    @Override')
        w('    public void renderToBuffer(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay,')
        w('                               float red, float green, float blue, float alpha) {')
        w('        root.render(poseStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);')
        w('    }')
        w('}')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w') as f:
            f.write('\n'.join(L) + '\n')
        print(f'wrote {out_path} ({len(self.cubes)} cubes, {len(order)} bones)')




def cube_list_lines(cs, targets):
    """Emit addOrReplaceChild lines for a CubeSet. targets: bone-path -> java var name.
    Each cube becomes a child bone with one box (no double offset):
    plain cubes -> bone at corner, box from (0,0,0); rotated cubes -> bone at the
    box center, box centered on the origin (rotation around the cube center)."""
    L = []
    for c in cs.cubes:
        u, v = c['uv']
        cw, ch, cd = (max(1, int(math.floor(x))) for x in c['s'])
        x, y, z = c['o']
        inflate = c.get('inflate', 0)
        defstr = f', new CubeDeformation({inflate}f)' if inflate else ''
        target = targets[c['bone']]
        rot = c.get('rot')
        if rot:
            pose = (f'PartPose.offsetAndRotation({x + cw / 2}F, {y + ch / 2}F, {z + cd / 2}F,'
                    f' {rot[0]}F, {rot[1]}F, {rot[2]}F)')
            bx, by, bz = -cw / 2, -ch / 2, -cd / 2
        else:
            pose = f'PartPose.offset({x}F, {y}F, {z}F)'
            bx, by, bz = 0, 0, 0
        L.append(f'        {target}.addOrReplaceChild("{c["name"]}", CubeListBuilder.create()')
        L.append(f'            .texOffs({u}, {v}).addBox({bx}F, {by}F, {bz}F, {cw}F, {ch}F, {cd}F{defstr}),')
        L.append(f'            {pose});')
    return L

# ------------------------------------------------------------------ painters
# painter(x, y, w, h, face, cube_name) -> RGBA or None
def metal(base, hi, dk, seed=7, scratch=0.06):
    def p(x, y, w, h, face, name):
        n = h01(x, y, seed + (hash(name) & 15))
        c = base
        if y == 0 or n > 0.9:
            c = hi
        elif y == h - 1 or n < 0.12:
            c = dk
        if h01(x, y, seed + 31) < scratch:
            c = mixc(c, hi, 0.6)
        return c
    return p

def leather(base, hi, dk, seed=5):
    def p(x, y, w, h, face, name):
        n = h01(x, y, seed)
        c = base
        if n > 0.86:
            c = hi
        elif n < 0.16:
            c = dk
        if y == 0:
            c = hi
        if y == h - 1:
            c = dk
        return c
    return p

def cloth(base, dk, hi, seed=3, fold=4):
    def p(x, y, w, h, face, name):
        n = vnoise(x, y // fold, seed)
        if n > 0.62:
            return mixc(base, hi, 0.4)
        if n < 0.34:
            return mixc(base, dk, 0.5)
        return base
    return p

def vertical_cols(base, hi, dk, seam, seed=11, period=4):
    """Columnar stone: vertical striations, dark seams between columns."""
    def p(x, y, w, h, face, name):
        col = x % period
        c = base
        if col == 0:
            c = seam
        elif col == 1:
            c = mixc(base, hi, 0.35)
        elif col == period - 1:
            c = mixc(base, dk, 0.5)
        n = h01(x, y, seed)
        if n > 0.93:
            c = mixc(c, hi, 0.5)
        elif n < 0.08:
            c = mixc(c, dk, 0.6)
        return c
    return p

def rough_stone(base, hi, dk, seed=13):
    def p(x, y, w, h, face, name):
        n = vnoise(x, y, seed, 2)
        if n > 0.66:
            c = mixc(base, hi, 0.45)
        elif n < 0.3:
            c = mixc(base, dk, 0.55)
        else:
            c = base
        if h01(x, y, seed + 7) > 0.94:
            c = hi
        return c
    return p

def bark(base, hi, dk, seed=17):
    def p(x, y, w, h, face, name):
        n = vnoise(x, y * 2.2, seed, 2)
        if n > 0.62:
            c = mixc(base, hi, 0.5)
        elif n < 0.32:
            c = mixc(base, dk, 0.6)
        else:
            c = base
        if (x + y * 3) % 7 == 0:
            c = mixc(c, dk, 0.4)  # grain cracks
        return c
    return p

def lacquer(base, hi, dk, seam, seed=19):
    def p(x, y, w, h, face, name):
        n = vnoise(x * 0.7, y, seed, 2)
        c = base
        if n > 0.66:
            c = mixc(base, hi, 0.5)
        elif n < 0.3:
            c = mixc(base, dk, 0.55)
        if y == 0:
            c = hi
        elif y == 1:
            c = mixc(base, hi, 0.25)
        elif y == h - 1:
            c = seam
        return c
    return p

def gold_trim(base, hi, dk, seed=23):
    def p(x, y, w, h, face, name):
        n = h01(x, y, seed)
        c = base
        if n > 0.78:
            c = hi
        elif n < 0.18:
            c = dk
        if y == 0:
            c = hi
        if y == h - 1:
            c = dk
        return c
    return p

def leaf(base, vein, dk, seed=29):
    def p(x, y, w, h, face, name):
        c = base
        cx = abs(x - (w - 1) / 2)
        if cx < 0.9:
            c = vein
        elif cx < 1.6:
            c = mixc(base, dk, 0.5)
        n = vnoise(x, y, seed, 2)
        if n > 0.75:
            c = mixc(c, hi_of(base), 0.4)
        if y == h - 1:
            c = dk
        return c
    return p

def hi_of(c):
    return shadec(c, 1.35)

def magma(base_dark, red, orange, yellow, seed=31, density=0.22):
    """Dark material with recessed magma cracks."""
    def p(x, y, w, h, face, name):
        n = vnoise(x, y, seed, 2)
        if n > 1 - density:
            t = (n - (1 - density)) / density
            if t > 0.66:
                return yellow if h01(x, y, seed) > 0.7 else orange
            if t > 0.33:
                return orange
            return red
        if n > 0.6:
            return mixc(base_dark, shadec(base_dark, 1.4), 0.5)
        if n < 0.3:
            return mixc(base_dark, shadec(base_dark, 0.6), 0.5)
        return base_dark
    return p

def emissive_mask(color, seed=41, density=0.16, hot=None):
    """Emissive island: scattered crack pixels."""
    def p(x, y, w, h, face, name):
        n = vnoise(x, y, seed, 2)
        if n > 1 - density:
            t = (n - (1 - density)) / density
            if t > 0.6 and hot:
                return hot
            return color
        return None
    return p

def moss_overlay(inner, moss, seed=47, density=0.14):
    def p(x, y, w, h, face, name):
        c = inner(x, y, w, h, face, name)
        if vnoise(x, y, seed, 2) < density:
            return mixc(c, moss, 0.55 + h01(x, y, seed) * 0.4)
        return c
    return p

def lichen_overlay(inner, lichen, seed=53, density=0.06):
    def p(x, y, w, h, face, name):
        c = inner(x, y, w, h, face, name)
        if vnoise(x * 1.7, y * 1.3, seed, 2) < density:
            return mixc(c, lichen, 0.7)
        return c
    return p
