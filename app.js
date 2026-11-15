const videoInput = document.querySelector('#videoInput');
const dropZone = document.querySelector('#dropZone');
const browseButton = document.querySelector('#browseButton');
const fileInfo = document.querySelector('#fileInfo');
const fileName = document.querySelector('#fileName');
const fileSize = document.querySelector('#fileSize');
const videoPreview = document.querySelector('#videoPreview');
const previewWrap = document.querySelector('#previewWrap');
const scanButton = document.querySelector('#scanButton');
const formMessage = document.querySelector('#formMessage');
const reportEmpty = document.querySelector('#reportEmpty');
const reportResults = document.querySelector('#reportResults');
const reportTimestamp = document.querySelector('#reportTimestamp');
const videosCount = document.querySelector('#videosCount');
const toast = document.querySelector('#toast');
const menuButton = document.querySelector('#menuButton');
const sidebar = document.querySelector('#sidebar');

let currentVideoUrl = null;
let toastTimer;
const MAX_FILE_SIZE = 500 * 1024 * 1024;

function formatBytes(bytes) {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3200);
}

function resetReport() {
  reportEmpty.hidden = false;
  reportResults.hidden = true;
  reportTimestamp.textContent = 'Waiting for a video';
}

function clearVideo() {
  videoPreview.pause();
  videoPreview.removeAttribute('src');
  videoPreview.load();
  if (currentVideoUrl) URL.revokeObjectURL(currentVideoUrl);
  currentVideoUrl = null;
  fileInfo.hidden = true;
  fileInfo.style.display = 'none';
  previewWrap.hidden = true;
  previewWrap.style.display = 'none';
  dropZone.hidden = false;
  dropZone.style.display = 'flex';
  scanButton.disabled = true;
  formMessage.textContent = '';
  videoInput.value = '';
  videosCount.innerHTML = '0 <span>videos added</span>';
  resetReport();
}

function useFile(file) {
  formMessage.textContent = '';
  if (!file) return;
  if (!file.type.startsWith('video/')) {
    formMessage.textContent = 'Please choose a valid video file.';
    return;
  }
  if (file.size > MAX_FILE_SIZE) {
    formMessage.textContent = 'This prototype supports files up to 500 MB.';
    return;
  }
  if (currentVideoUrl) URL.revokeObjectURL(currentVideoUrl);
  currentVideoUrl = URL.createObjectURL(file);
  videoPreview.src = currentVideoUrl;
  fileName.textContent = file.name;
  fileSize.textContent = `${formatBytes(file.size)} · Stored in this browser only`;
  dropZone.hidden = true;
  dropZone.style.display = 'none';
  fileInfo.hidden = false;
  fileInfo.style.display = 'flex';
  previewWrap.hidden = false;
  previewWrap.style.display = 'block';
  scanButton.disabled = false;
  videosCount.innerHTML = '1 <span>video added</span>';
  resetReport();
}

browseButton.addEventListener('click', (event) => {
  event.stopPropagation();
  videoInput.click();
});
dropZone.addEventListener('click', (event) => {
  if (event.target !== browseButton) videoInput.click();
});
dropZone.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    videoInput.click();
  }
});
videoInput.addEventListener('change', () => useFile(videoInput.files[0]));
['dragenter', 'dragover'].forEach((eventName) => dropZone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropZone.classList.add('drag-over');
}));
['dragleave', 'drop'].forEach((eventName) => dropZone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropZone.classList.remove('drag-over');
}));
dropZone.addEventListener('drop', (event) => useFile(event.dataTransfer.files[0]));
document.querySelector('#removeFile').addEventListener('click', clearVideo);

scanButton.addEventListener('click', () => {
  if (!currentVideoUrl) return;
  reportEmpty.hidden = true;
  reportResults.hidden = false;
  reportTimestamp.textContent = 'Demo view · just now';
  showToast('Demo preview shown — no video analysis was performed.');
  document.querySelector('#report').scrollIntoView({ behavior: 'smooth', block: 'center' });
});

menuButton.addEventListener('click', () => {
  const isOpen = sidebar.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(isOpen));
});
document.querySelectorAll('.nav-link').forEach((link) => link.addEventListener('click', () => {
  sidebar.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
}));
document.addEventListener('click', (event) => {
  if (window.innerWidth <= 760 && sidebar.classList.contains('open') && !sidebar.contains(event.target) && !menuButton.contains(event.target)) {
    sidebar.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  }
});
window.addEventListener('beforeunload', () => {
  if (currentVideoUrl) URL.revokeObjectURL(currentVideoUrl);
});
