const groupNumberEl = document.getElementById('group-number');
const projectTitleEl = document.getElementById('project-title');
const groupMembersEl = document.getElementById('group-members');
const form = document.getElementById('project-form');

const STORAGE_KEY = 'capstoneProjectPlaceholders';

function loadFromStorage() {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) return null;
    return JSON.parse(stored);
  } catch (error) {
    console.warn('Unable to load saved placeholders', error);
    return null;
  }
}

function saveToStorage(value) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
  } catch (error) {
    console.warn('Unable to save placeholders', error);
  }
}

function applyValues({ groupNumber, projectTitle, groupMembers }) {
  groupNumberEl.textContent = groupNumber || '[GroupNumber]';
  projectTitleEl.textContent = projectTitle || '[ProjectTitle]';
  groupMembersEl.textContent = groupMembers || '[Group Members]';
}

function init() {
  const values = loadFromStorage();
  if (values) {
    applyValues(values);
    document.getElementById('input-group-number').value = values.groupNumber || '';
    document.getElementById('input-project-title').value = values.projectTitle || '';
    document.getElementById('input-group-members').value = values.groupMembers || '';
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const newValues = {
    groupNumber: document.getElementById('input-group-number').value.trim(),
    projectTitle: document.getElementById('input-project-title').value.trim(),
    groupMembers: document.getElementById('input-group-members').value.trim(),
  };

  applyValues(newValues);
  saveToStorage(newValues);
});

init();
