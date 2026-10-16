package com.opus.paradise.world;

public final class ParadiseSpawns {
    private ParadiseSpawns() { }

    public static void init() {
        ParadiseWildlifeSpawner.init();
        ParadiseIslandSpawner.init();
    }
}
