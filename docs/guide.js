(() => {
  const catalog = window.OPUS_CATALOG || { recipes: [], entries: [] };
  const entries = new Map((catalog.entries || []).map(entry => [entry.id, entry]));
  const recipeGrid = document.querySelector('#recipe-grid');
  const recipeSearch = document.querySelector('#recipe-search');
  const recipeFilter = document.querySelector('#recipe-filter');
  const recipeSummary = document.querySelector('#recipe-summary');
  const guideSearch = document.querySelector('#guide-search');
  const nav = [...document.querySelectorAll('.sidebar nav a')];

  const shortId = value => {
    if (!value) return '';
    const first = String(value).split(' / ')[0];
    return first.includes(':') ? first.split(':')[1] : first;
  };

  function iconFor(value, alt = '') {
    const entry = entries.get(shortId(value));
    if (entry && entry.image) return `<img src="${entry.image}" alt="${alt || entry.name}" loading="lazy">`;
    return `<span class="no-icon">${shortId(value).slice(0, 4)}</span>`;
  }

  function cell(value) {
    if (!value) return '<span class="cell empty"></span>';
    const name = typeof value === 'string' ? value : value.name;
    const id = typeof value === 'string' ? value : value.id;
    return `<span class="cell" title="${name || id}">${iconFor(id, name)}</span>`;
  }

  function gridFor(recipe) {
    const cells = [];
    if (recipe.pattern) {
      const key = recipe.key || {};
      for (let row = 0; row < 5; row++) {
        for (let col = 0; col < 5; col++) {
          const symbol = recipe.pattern[row] && recipe.pattern[row][col];
          // '#' is a valid recipe key in Minecraft JSON, not an empty cell.
          cells.push(symbol ? cell(key[symbol]) : '<span class="cell empty"></span>');
        }
      }
    } else {
      const ingredients = recipe.ingredients || [];
      for (let index = 0; index < 25; index++) cells.push(cell(ingredients[index]));
    }
    return `<div class="grid" aria-label="Схема рецепта">${cells.join('')}</div>`;
  }

  function recipeCard(recipe) {
    const ingredients = recipe.ingredients || Object.values(recipe.key || {});
    const ingredientList = ingredients.slice(0, 8).map(value => {
      const name = typeof value === 'string' ? value : value.name;
      return `<div>• <b>${name || value.id}</b></div>`;
    }).join('') || '<div>• Схема по ключу рецепта</div>';
    return `<article class="recipe-card searchable" data-search="${[recipe.id, recipe.name, recipe.type, recipe.result].join(' ').toLowerCase()}">
      <div class="recipe-top"><div><div class="recipe-type">${recipe.type}</div><h3>${recipe.name}</h3><small>${recipe.id}</small></div><div class="result" title="Результат">${iconFor(recipe.result, recipe.name)}</div></div>
      <div class="recipe-body">${gridFor(recipe)}<div class="ingredient-list">${ingredientList}</div></div>
      ${recipe.catalyst ? '<p class="recipe-note">Катализатор возвращается после ковки</p>' : ''}
    </article>`;
  }

  function renderRecipes() {
    const query = (recipeSearch.value || '').trim().toLowerCase();
    const filter = recipeFilter.value;
    const list = (catalog.recipes || []).filter(recipe => {
      const ingredients = [...(recipe.ingredients || []), ...Object.values(recipe.key || {})]
        .flatMap(value => typeof value === 'string' ? [value] : [value.id, value.name]);
      const resultName = entries.get(shortId(recipe.result))?.name || '';
      const searchText = [recipe.id, recipe.name, recipe.type, recipe.result, resultName, ...ingredients]
        .filter(Boolean).join(' ').toLowerCase();
      const matchesQuery = !query || searchText.includes(query);
      return matchesQuery && (filter === 'all' || recipe.type === filter);
    });
    recipeSummary.textContent = `Показано ${list.length} из ${(catalog.recipes || []).length} рецептов · схемы отображаются в сетке 5×5`;
    recipeGrid.innerHTML = list.map(recipeCard).join('') || '<p class="empty-result">Ничего не найдено. Попробуйте другой запрос.</p>';
  }

  function filterSections() {
    const query = (guideSearch.value || '').trim().toLowerCase();
    document.querySelectorAll('.section.searchable').forEach(section => {
      if (!query) section.hidden = false;
      else section.hidden = !(`${section.dataset.search || ''} ${section.textContent}`.toLowerCase().includes(query));
    });
  }

  recipeSearch?.addEventListener('input', renderRecipes);
  recipeFilter?.addEventListener('change', renderRecipes);
  guideSearch?.addEventListener('input', filterSections);
  document.addEventListener('keydown', event => {
    if (event.key === '/' && document.activeElement.tagName !== 'INPUT') {
      event.preventDefault();
      guideSearch?.focus();
    }
  });

  const menuButton = document.querySelector('#menu-button');
  const sidebar = document.querySelector('#sidebar');
  menuButton?.addEventListener('click', () => {
    const open = sidebar.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  nav.forEach(link => link.addEventListener('click', () => sidebar.classList.remove('open')));

  const sections = [...document.querySelectorAll('main > section, main > header')];
  const observer = new IntersectionObserver(items => {
    const visible = items.filter(item => item.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    const id = visible.target.id;
    nav.forEach(link => link.classList.toggle('active', link.getAttribute('href') === `#${id}`));
  }, { rootMargin: '-15% 0px -70% 0px', threshold: [0, .2, .6] });
  sections.forEach(section => observer.observe(section));
  window.addEventListener('scroll', () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    document.querySelector('#reading-progress').style.width = `${max > 0 ? scrollY / max * 100 : 0}%`;
  }, { passive: true });
  renderRecipes();
})();
