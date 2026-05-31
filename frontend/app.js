const budgetInput = document.getElementById("budget");
const budgetValue = document.getElementById("budgetValue");
const systemBar = document.getElementById("systemBar");
const contextBar = document.getElementById("contextBar");
const userBar = document.getElementById("userBar");
const contextBarLabel = document.getElementById("contextBarLabel");
const userLegend = document.getElementById("userLegend");
const budgetNarrative = document.getElementById("budgetNarrative");
const compressionList = document.getElementById("compressionList");

function setSegment(bar, percent, label) {
  bar.style.width = `${percent}%`;
  bar.querySelector(".bar-label").textContent = label;
  bar.classList.toggle("compact", percent < 12);
}

function renderBudget() {
  const budget = Number(budgetInput.value);
  const system = 800;
  const user = 200;
  const context = Math.max(700, Math.round((budget - 1000) * 0.95));
  const total = system + user + context;
  const systemPct = (system / budget) * 100;
  const userPct = (user / budget) * 100;
  const contextPct = Math.max(0, 100 - systemPct - userPct);

  budgetValue.textContent = String(budget);
  setSegment(systemBar, systemPct, `System ${system}`);
  setSegment(contextBar, contextPct, `Context ${context}`);
  setSegment(userBar, userPct, `User ${user}`);
  contextBarLabel.textContent = `Context ${context}`;
  userLegend.textContent = `User reserve ${user}`;

  if (budget >= 3400) {
    budgetNarrative.textContent = `Total ${total} / ${budget}. Fits with protected constraints untouched.`;
    compressionList.innerHTML = `
      <li>Pass 1: low-value facts collapse from FULL to CONSTRAINT_ONLY</li>
      <li>Pass 2: medium-value decisions compress to COMPRESSED</li>
      <li>Constraints remain FULL regardless of distance</li>
    `;
  } else if (budget >= 2600) {
    budgetNarrative.textContent = `Total ${total} / ${budget}. More decisions compress, but safety constraints remain full.`;
    compressionList.innerHTML = `
      <li>Pass 1: distant facts are omitted first</li>
      <li>Pass 2: medium injection-weight decisions summarize aggressively</li>
      <li>Protected constraints still hold their full payload</li>
    `;
  } else {
    budgetNarrative.textContent = `Total pressure is high at ${budget}. The engine would omit most non-constraints and raise human review if protected constraints alone overflow.`;
    compressionList.innerHTML = `
      <li>Pass 1: most facts are omitted</li>
      <li>Pass 2: decisions shrink to minimal summaries</li>
      <li>If constraints alone do not fit, human review is required</li>
    `;
  }
}

budgetInput.addEventListener("input", renderBudget);
renderBudget();
