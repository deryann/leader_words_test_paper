async function fetchConfigs() {
  const res = await fetch('/api/configs');
  if (!res.ok) {
    console.error('Failed to fetch configs');
    return [];
  }
  return await res.json();
}

async function generate() {
  const select = document.getElementById('configSelect');
  const config = select.value;
  if (!config) {
    alert('Please select a config file');
    return;
  }
  const format = document.querySelector('input[name="format"]:checked').value;
  const url = `/api/generate?config=${encodeURIComponent(config)}&format=${encodeURIComponent(format)}`;
  const res = await fetch(url);
  if (!res.ok) {
    const error = await res.json();
    alert(`Error: ${error.detail}`);
    return;
  }
  const data = await res.json();
  const linksDiv = document.getElementById('links');
  linksDiv.innerHTML = '';
  const testLink = document.createElement('a');
  testLink.href = data.test.url;
  testLink.textContent = `Download Test Paper (${format.toUpperCase()})`;
  linksDiv.appendChild(testLink);
  const ansLink = document.createElement('a');
  ansLink.href = data.ans.url;
  ansLink.textContent = `Download Answer Sheet (${format.toUpperCase()})`;
  linksDiv.appendChild(ansLink);
}

document.getElementById('generateBtn').addEventListener('click', generate);

window.addEventListener('load', async () => {
  const configs = await fetchConfigs();
  const select = document.getElementById('configSelect');
  configs.forEach(cfg => {
    const opt = document.createElement('option');
    opt.value = cfg;
    opt.textContent = cfg;
    select.appendChild(opt);
  });
});