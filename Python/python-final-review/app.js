const STORE_KEY = "pythonFinalReviewProgress.v1";

const typeNames = {
  choice: "选择题",
  fill: "填空题",
  debug: "纠错题",
  code: "编程题"
};

const sourceNames = {
  "样卷": "样卷",
  "作业": "作业",
  "复习题(2)": "复习题(2)",
  "教材第7章": "教材",
  "教材第8章": "教材",
  "教材第11章": "教材"
};

let state = loadState();
let currentQuestion = null;
let answeredCurrent = false;

const el = {
  answeredCount: document.querySelector("#answeredCount"),
  accuracyRate: document.querySelector("#accuracyRate"),
  masteredCount: document.querySelector("#masteredCount"),
  totalQuestionCount: document.querySelector("#totalQuestionCount"),
  wrongCount: document.querySelector("#wrongCount"),
  topicFilter: document.querySelector("#topicFilter"),
  typeFilter: document.querySelector("#typeFilter"),
  modeSelect: document.querySelector("#modeSelect"),
  resetFilters: document.querySelector("#resetFilters"),
  resetProgress: document.querySelector("#resetProgress"),
  recommendationTitle: document.querySelector("#recommendationTitle"),
  weakTopicList: document.querySelector("#weakTopicList"),
  typeChip: document.querySelector("#typeChip"),
  topicChip: document.querySelector("#topicChip"),
  sourceChip: document.querySelector("#sourceChip"),
  questionCounter: document.querySelector("#questionCounter"),
  questionPrompt: document.querySelector("#questionPrompt"),
  questionCode: document.querySelector("#questionCode"),
  answerForm: document.querySelector("#answerForm"),
  feedbackPanel: document.querySelector("#feedbackPanel"),
  feedbackTitle: document.querySelector("#feedbackTitle"),
  feedbackBody: document.querySelector("#feedbackBody"),
  submitAnswer: document.querySelector("#submitAnswer"),
  revealAnswer: document.querySelector("#revealAnswer"),
  nextQuestion: document.querySelector("#nextQuestion"),
  topicGrid: document.querySelector("#topicGrid"),
  wrongList: document.querySelector("#wrongList")
};

init();

function init() {
  populateTopics();
  bindEvents();
  switchView("practice");
  pickQuestion();
  renderAll();
}

function loadState() {
  try {
    const stored = localStorage.getItem(STORE_KEY);
    if (stored) return JSON.parse(stored);
  } catch (error) {
    console.warn("无法读取本地进度", error);
  }
  return {
    progress: {},
    orderedIndex: 0,
    lastQuestionId: null
  };
}

function saveState() {
  localStorage.setItem(STORE_KEY, JSON.stringify(state));
}

function populateTopics() {
  el.topicFilter.innerHTML = [
    `<option value="all">全部知识点</option>`,
    ...window.REVIEW_TOPICS.map((topic) => `<option value="${topic.id}">${escapeHtml(topic.name)}</option>`)
  ].join("");
}

function bindEvents() {
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.view));
  });

  [el.topicFilter, el.typeFilter, el.modeSelect].forEach((control) => {
    control.addEventListener("change", () => {
      state.orderedIndex = 0;
      pickQuestion();
      renderAll();
    });
  });

  el.resetFilters.addEventListener("click", () => {
    el.topicFilter.value = "all";
    el.typeFilter.value = "all";
    el.modeSelect.value = "adaptive";
    state.orderedIndex = 0;
    pickQuestion();
    renderAll();
  });

  el.resetProgress.addEventListener("click", () => {
    if (!confirm("确定清空所有答题记录吗？")) return;
    state = { progress: {}, orderedIndex: 0, lastQuestionId: null };
    saveState();
    pickQuestion();
    renderAll();
  });

  el.submitAnswer.addEventListener("click", submitAnswer);
  el.revealAnswer.addEventListener("click", revealAnswer);
  el.nextQuestion.addEventListener("click", () => {
    answeredCurrent = false;
    pickQuestion(true);
    renderAll();
  });
}

function switchView(viewName) {
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === viewName);
  });
  document.querySelectorAll(".view").forEach((view) => {
    view.classList.remove("is-visible");
  });
  document.querySelector(`#${viewName}View`).classList.add("is-visible");
  renderSummary();
  renderTopicMap();
  renderWrongList();
}

function getFilteredQuestions() {
  const topic = el.topicFilter.value;
  const type = el.typeFilter.value;
  return window.REVIEW_QUESTIONS.filter((question) => {
    if (!question || typeof question.prompt !== "string" || question.prompt.trim() === "") return false;
    const topicOk = topic === "all" || question.topic === topic;
    const typeOk = type === "all" || question.type === type;
    return topicOk && typeOk;
  });
}

function pickQuestion(advance = false) {
  const questions = getFilteredQuestions();
  if (questions.length === 0) {
    currentQuestion = null;
    return;
  }

  const mode = el.modeSelect.value;
  if (mode === "ordered") {
    if (advance) state.orderedIndex += 1;
    state.orderedIndex = state.orderedIndex % questions.length;
    currentQuestion = questions[state.orderedIndex];
  } else if (mode === "shuffle") {
    currentQuestion = randomQuestion(questions);
  } else {
    currentQuestion = adaptiveQuestion(questions);
  }

  state.lastQuestionId = currentQuestion.id;
  saveState();
}

function randomQuestion(questions) {
  if (questions.length === 1) return questions[0];
  const pool = questions.filter((question) => question.id !== state.lastQuestionId);
  return pool[Math.floor(Math.random() * pool.length)];
}

function adaptiveQuestion(questions) {
  const stats = getTopicStats();
  const scored = questions.map((question) => {
    const progress = state.progress[question.id];
    const topicStat = stats.byTopic[question.topic];
    const topicAccuracy = topicStat.attempts ? topicStat.correct / topicStat.attempts : 0;
    let score = Math.random() * 20;
    if (!progress) score += 900;
    if (progress && !progress.lastCorrect) score += 550;
    if (progress && progress.revealed) score += 260;
    score += (1 - topicAccuracy) * 220;
    score -= progress ? progress.correct * 45 : 0;
    if (question.id === state.lastQuestionId && questions.length > 1) score -= 120;
    return { question, score };
  });
  scored.sort((a, b) => b.score - a.score);
  return scored[0].question;
}

function renderAll() {
  renderSummary();
  renderQuestion();
  renderRecommendation();
  renderTopicMap();
  renderWrongList();
}

function renderSummary() {
  const stats = getTopicStats();
  el.answeredCount.textContent = String(stats.totalAttempts);
  el.accuracyRate.textContent = stats.totalAttempts ? `${Math.round((stats.totalCorrect / stats.totalAttempts) * 100)}%` : "0%";
  el.masteredCount.textContent = String(stats.masteredTopics);
  if (el.totalQuestionCount) el.totalQuestionCount.textContent = String(window.REVIEW_QUESTIONS.length);
  if (el.wrongCount) el.wrongCount.textContent = String(stats.activeWrong);
}

function renderRecommendation() {
  const weak = getWeakTopics();
  if (weak.length === 0) {
    el.recommendationTitle.textContent = "先做一题诊断";
    el.weakTopicList.innerHTML = `<span class="weak-pill">系统会自动记录薄弱点</span>`;
    return;
  }

  el.recommendationTitle.textContent = `优先复习：${weak[0].name}`;
  el.weakTopicList.innerHTML = weak
    .slice(0, 4)
    .map((topic) => `<span class="weak-pill">${escapeHtml(topic.name)} ${Math.round(topic.accuracy * 100)}%</span>`)
    .join("");
}

function renderQuestion() {
  answeredCurrent = false;
  el.feedbackPanel.className = "feedback-panel hidden";
  el.feedbackTitle.textContent = "";
  el.feedbackBody.innerHTML = "";

  if (!currentQuestion) {
    el.questionPrompt.textContent = "当前筛选下没有题目";
    el.questionCode.classList.add("hidden");
    el.answerForm.innerHTML = `<div class="empty-state">换一个知识点或题型继续练。</div>`;
    return;
  }

  const questions = getFilteredQuestions();
  const index = questions.findIndex((question) => question.id === currentQuestion.id);
  const topic = getTopic(currentQuestion.topic);
  el.typeChip.textContent = typeNames[currentQuestion.type];
  el.topicChip.textContent = topic.name;
  el.sourceChip.textContent = shortSource(currentQuestion.source);
  el.questionCounter.textContent = `${index + 1} / ${questions.length}`;
  el.questionPrompt.textContent = currentQuestion.prompt;

  if (currentQuestion.code) {
    el.questionCode.textContent = currentQuestion.code;
    el.questionCode.classList.remove("hidden");
  } else {
    el.questionCode.classList.add("hidden");
  }

  if (currentQuestion.type === "choice") renderChoice(currentQuestion);
  if (currentQuestion.type === "fill") renderFill(currentQuestion);
  if (currentQuestion.type === "debug") renderDebug(currentQuestion);
  if (currentQuestion.type === "code") renderCode(currentQuestion);
}

function renderChoice(question) {
  el.answerForm.innerHTML = question.options
    .map(
      (option) => `
        <label class="option-row">
          <input type="radio" name="choice" value="${option.id}" />
          <span><strong>${option.id}.</strong> ${escapeHtml(option.text)}</span>
        </label>
      `
    )
    .join("");
}

function renderFill(question) {
  el.answerForm.innerHTML = `
    <div class="blank-grid">
      ${question.blanks
        .map(
          (blank, index) => `
            <label>
              ${escapeHtml(blank.label || `第 ${index + 1} 空`)}
              <input type="text" data-blank-index="${index}" autocomplete="off" />
            </label>
          `
        )
        .join("")}
    </div>
  `;
}

function renderCode() {
  el.answerForm.innerHTML = `
    <label>
      代码答案
      <textarea class="code-answer" id="codeAnswer" spellcheck="false" placeholder="在这里写 Python 代码"></textarea>
    </label>
  `;
}

function renderDebug(question) {
  el.answerForm.innerHTML = `
    <div class="debug-grid">
      <label>
        错误代码
        <input type="text" data-debug-field="wrong" autocomplete="off" placeholder="${escapeHtml(question.debug?.wrongPlaceholder || "例如：count =+ 1")}" />
      </label>
      <label>
        正确代码
        <input type="text" data-debug-field="fixed" autocomplete="off" placeholder="${escapeHtml(question.debug?.fixedPlaceholder || "例如：count += 1")}" />
      </label>
    </div>
  `;
}

function submitAnswer() {
  if (!currentQuestion || answeredCurrent) return;
  const result = evaluateCurrent();
  if (!result) return;
  answeredCurrent = true;
  recordAttempt(currentQuestion, result);
  showFeedback(result);
  renderSummary();
  renderRecommendation();
  renderTopicMap();
  renderWrongList();
}

function evaluateCurrent() {
  if (currentQuestion.type === "choice") {
    const selected = el.answerForm.querySelector("input[name='choice']:checked");
    if (!selected) {
      showNotice("还没有选择答案。");
      return null;
    }
    const correct = selected.value === currentQuestion.answer;
    return {
      correct,
      score: correct ? 100 : 0,
      given: selected.value,
      expected: currentQuestion.answer,
      details: []
    };
  }

  if (currentQuestion.type === "fill") {
    const inputs = [...el.answerForm.querySelectorAll("input[data-blank-index]")];
    const details = inputs.map((input, index) => {
      const blank = currentQuestion.blanks[index];
      const given = normalizeAnswer(input.value);
      const expected = blank.answers.map(normalizeAnswer);
      const correct = expected.includes(given);
      return {
        label: blank.label || `第 ${index + 1} 空`,
        correct,
        given: input.value,
        expected: blank.answers.join(" 或 ")
      };
    });
    const correctCount = details.filter((item) => item.correct).length;
    return {
      correct: correctCount === details.length,
      score: Math.round((correctCount / details.length) * 100),
      given: details.map((item) => item.given).join(" | "),
      expected: details.map((item) => item.expected).join(" | "),
      details
    };
  }

  if (currentQuestion.type === "code") {
    const textarea = document.querySelector("#codeAnswer");
    const code = textarea.value.trim();
    if (!code) {
      showNotice("先写一点代码再提交。");
      return null;
    }
    const details = currentQuestion.criteria.map((criterion) => evaluateCriterion(code, criterion));
    const score = details.reduce((sum, item) => sum + item.earned, 0);
    return {
      correct: score >= 70,
      score,
      given: code,
      expected: currentQuestion.sampleAnswer,
      details
    };
  }

  if (currentQuestion.type === "debug") {
    const wrongInput = el.answerForm.querySelector("[data-debug-field='wrong']");
    const fixedInput = el.answerForm.querySelector("[data-debug-field='fixed']");
    const wrongGiven = wrongInput.value;
    const fixedGiven = fixedInput.value;
    const wrongOk = currentQuestion.debug.wrongAnswers.map(normalizeCodeLine).includes(normalizeCodeLine(wrongGiven));
    const fixedOk = currentQuestion.debug.fixedAnswers.map(normalizeCodeLine).includes(normalizeCodeLine(fixedGiven));
    const details = [
      {
        label: "错误代码",
        correct: wrongOk,
        given: wrongGiven,
        expected: currentQuestion.debug.wrongAnswers.join(" 或 ")
      },
      {
        label: "正确代码",
        correct: fixedOk,
        given: fixedGiven,
        expected: currentQuestion.debug.fixedAnswers.join(" 或 ")
      }
    ];
    const correctCount = details.filter((item) => item.correct).length;
    return {
      correct: wrongOk && fixedOk,
      score: correctCount * 50,
      given: `${wrongGiven} -> ${fixedGiven}`,
      expected: `${currentQuestion.debug.wrongAnswers[0]} -> ${currentQuestion.debug.fixedAnswers[0]}`,
      details
    };
  }

  return null;
}

function evaluateCriterion(code, criterion) {
  const allOk = (criterion.all || []).every((pattern) => patternMatches(code, pattern));
  const anyList = criterion.any || [];
  const anyOk = anyList.length === 0 || anyList.some((pattern) => patternMatches(code, pattern));
  const passed = allOk && anyOk;
  return {
    label: criterion.label,
    points: criterion.points,
    earned: passed ? criterion.points : 0,
    passed
  };
}

function patternMatches(code, pattern) {
  try {
    return new RegExp(pattern, "is").test(code);
  } catch (error) {
    return code.includes(pattern);
  }
}

function revealAnswer() {
  if (!currentQuestion) return;
  if (!answeredCurrent) {
    answeredCurrent = true;
    recordAttempt(currentQuestion, {
      correct: false,
      score: 0,
      revealed: true,
      given: "查看答案",
      expected: getExpectedAnswer(currentQuestion),
      details: []
    });
  }
  showAnswerOnly();
  renderSummary();
  renderRecommendation();
  renderTopicMap();
  renderWrongList();
}

function recordAttempt(question, result) {
  const progress = state.progress[question.id] || {
    attempts: 0,
    correct: 0,
    mistakes: 0,
    lastScore: 0,
    lastCorrect: false,
    revealed: false,
    lastGiven: "",
    lastAt: ""
  };

  progress.attempts += 1;
  if (result.correct) progress.correct += 1;
  if (!result.correct) progress.mistakes += 1;
  progress.lastScore = result.score;
  progress.lastCorrect = result.correct;
  progress.revealed = Boolean(result.revealed);
  progress.lastGiven = result.given || "";
  progress.lastAt = new Date().toISOString();
  state.progress[question.id] = progress;
  saveState();
}

function showFeedback(result) {
  el.feedbackPanel.className = `feedback-panel ${result.correct ? "correct" : "incorrect"}`;
  el.feedbackTitle.textContent = result.correct ? `答对了，得分 ${result.score}` : `还差一点，得分 ${result.score}`;

  let body = "";
  if (currentQuestion.type === "choice") {
    body = `
      <p>你的答案：${escapeHtml(result.given)}；正确答案：${escapeHtml(result.expected)}。</p>
      <p>${escapeHtml(currentQuestion.explanation)}</p>
    `;
  } else if (currentQuestion.type === "fill") {
    body = `
      <div class="criteria-list">
        ${result.details
          .map(
            (item) => `
              <div class="criteria-row">
                <span>${escapeHtml(item.label)}：${escapeHtml(item.given || "未填")} / ${escapeHtml(item.expected)}</span>
                <strong>${item.correct ? "对" : "错"}</strong>
              </div>
            `
          )
          .join("")}
      </div>
      <p>${escapeHtml(currentQuestion.explanation)}</p>
    `;
  } else if (currentQuestion.type === "debug") {
    body = `
      <div class="criteria-list">
        ${result.details
          .map(
            (item) => `
              <div class="criteria-row">
                <span>${escapeHtml(item.label)}：${escapeHtml(item.given || "未填")} / ${escapeHtml(item.expected)}</span>
                <strong>${item.correct ? "对" : "错"}</strong>
              </div>
            `
          )
          .join("")}
      </div>
      <p>${escapeHtml(currentQuestion.explanation)}</p>
    `;
  } else {
    body = `
      <div class="criteria-list">
        ${result.details
          .map(
            (item) => `
              <div class="criteria-row">
                <span>${escapeHtml(item.label)}</span>
                <strong>${item.earned}/${item.points}</strong>
              </div>
            `
          )
          .join("")}
      </div>
      <p>${escapeHtml(currentQuestion.explanation)}</p>
      <pre class="code-block">${escapeHtml(currentQuestion.sampleAnswer)}</pre>
    `;
  }
  el.feedbackBody.innerHTML = body;
}

function showAnswerOnly() {
  el.feedbackPanel.className = "feedback-panel incorrect";
  el.feedbackTitle.textContent = "参考答案";
  let answer = "";
  if (currentQuestion.type === "choice") {
    answer = `正确答案：${currentQuestion.answer}\n\n${currentQuestion.explanation}`;
  } else if (currentQuestion.type === "fill") {
    answer = currentQuestion.blanks
      .map((blank) => `${blank.label}：${blank.answers[0]}`)
      .join("\n");
    answer += `\n\n${currentQuestion.explanation}`;
  } else if (currentQuestion.type === "debug") {
    answer = `错误代码：${currentQuestion.debug.wrongAnswers[0]}\n正确代码：${currentQuestion.debug.fixedAnswers[0]}\n\n${currentQuestion.explanation}`;
  } else {
    answer = `${currentQuestion.explanation}\n\n${currentQuestion.sampleAnswer}`;
  }
  el.feedbackBody.innerHTML = `<pre class="code-block">${escapeHtml(answer)}</pre>`;
}

function showNotice(text) {
  el.feedbackPanel.className = "feedback-panel incorrect";
  el.feedbackTitle.textContent = "还不能提交";
  el.feedbackBody.innerHTML = `<p>${escapeHtml(text)}</p>`;
}

function getExpectedAnswer(question) {
  if (question.type === "choice") return question.answer;
  if (question.type === "fill") return question.blanks.map((blank) => blank.answers[0]).join(" | ");
  if (question.type === "debug") return `${question.debug.wrongAnswers[0]} -> ${question.debug.fixedAnswers[0]}`;
  return question.sampleAnswer;
}

function renderTopicMap() {
  const stats = getTopicStats();
  el.topicGrid.innerHTML = window.REVIEW_TOPICS.map((topic) => {
    const topicStat = stats.byTopic[topic.id];
    const totalQuestions = window.REVIEW_QUESTIONS.filter((question) => question.topic === topic.id).length;
    const accuracy = topicStat.attempts ? topicStat.correct / topicStat.attempts : 0;
    const width = Math.round(accuracy * 100);
    const label = topicStat.attempts ? `${width}%` : "未诊断";
    return `
      <article class="topic-tile">
        <h3>${escapeHtml(topic.name)}</h3>
        <div class="meter" aria-label="${escapeHtml(topic.name)}掌握度">
          <span style="width: ${width}%"></span>
        </div>
        <div class="topic-meta">
          <span>${label}</span>
          <span>${topicStat.attempts} 次 / ${totalQuestions} 题</span>
        </div>
      </article>
    `;
  }).join("");
}

function renderWrongList() {
  const wrongQuestions = window.REVIEW_QUESTIONS.filter((question) => {
    const progress = state.progress[question.id];
    return progress && progress.mistakes > 0 && !progress.lastCorrect;
  });

  if (wrongQuestions.length === 0) {
    el.wrongList.innerHTML = `<div class="empty-state">暂时没有错题。做题后，这里会保留最近还没答对的题。</div>`;
    return;
  }

  el.wrongList.innerHTML = wrongQuestions
    .map((question) => {
      const progress = state.progress[question.id];
      return `
        <article class="wrong-item">
          <div class="chips">
            <span class="chip">${typeNames[question.type]}</span>
            <span class="chip topic-chip">${escapeHtml(getTopic(question.topic).name)}</span>
          </div>
          <h3>${escapeHtml(question.prompt)}</h3>
          ${question.code ? `<pre class="code-block">${escapeHtml(question.code)}</pre>` : ""}
          <p>最近得分：${progress.lastScore}；错误次数：${progress.mistakes}</p>
          <button class="ghost-button retry-button" data-question-id="${question.id}">重练这题</button>
        </article>
      `;
    })
    .join("");

  document.querySelectorAll(".retry-button").forEach((button) => {
    button.addEventListener("click", () => {
      currentQuestion = window.REVIEW_QUESTIONS.find((question) => question.id === button.dataset.questionId);
      answeredCurrent = false;
      switchView("practice");
      renderQuestion();
    });
  });
}

function getTopicStats() {
  const byTopic = Object.fromEntries(
    window.REVIEW_TOPICS.map((topic) => [topic.id, { attempts: 0, correct: 0, questions: 0 }])
  );
  let totalAttempts = 0;
  let totalCorrect = 0;

  window.REVIEW_QUESTIONS.forEach((question) => {
    byTopic[question.topic].questions += 1;
    const progress = state.progress[question.id];
    if (!progress) return;
    byTopic[question.topic].attempts += progress.attempts;
    byTopic[question.topic].correct += progress.correct;
    totalAttempts += progress.attempts;
    totalCorrect += progress.correct;
  });

  const masteredTopics = Object.values(byTopic).filter((topic) => {
    if (topic.attempts < 2) return false;
    return topic.correct / topic.attempts >= 0.8;
  }).length;
  const activeWrong = window.REVIEW_QUESTIONS.filter((question) => {
    const progress = state.progress[question.id];
    return progress && progress.mistakes > 0 && !progress.lastCorrect;
  }).length;

  return { byTopic, totalAttempts, totalCorrect, masteredTopics, activeWrong };
}

function getWeakTopics() {
  const stats = getTopicStats();
  return window.REVIEW_TOPICS
    .map((topic) => {
      const item = stats.byTopic[topic.id];
      const accuracy = item.attempts ? item.correct / item.attempts : 0;
      return { ...topic, attempts: item.attempts, accuracy };
    })
    .filter((topic) => topic.attempts > 0 && topic.accuracy < 0.8)
    .sort((a, b) => a.accuracy - b.accuracy || b.attempts - a.attempts);
}

function getTopic(topicId) {
  return window.REVIEW_TOPICS.find((topic) => topic.id === topicId) || { id: topicId, name: topicId };
}

function shortSource(source) {
  return sourceNames[source] || source.split(" ")[0];
}

function normalizeAnswer(value) {
  return String(value)
    .trim()
    .replace(/[，]/g, ",")
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/\s+/g, " ")
    .toLowerCase();
}

function normalizeCodeLine(value) {
  return String(value)
    .trim()
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/\s+/g, "");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
