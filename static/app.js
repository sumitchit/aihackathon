const form = document.getElementById('analysis-form');
const issuesList = document.getElementById('issues-list');
const reportOutput = document.getElementById('report-output');
const previewTableHead = document.querySelector('#preview-table thead');
const previewTableBody = document.querySelector('#preview-table tbody');
const rowCount = document.getElementById('row-count');
const columnCount = document.getElementById('column-count');
const issueCount = document.getElementById('issue-count');
const qualityPill = document.getElementById('quality-pill');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const fileInput = document.getElementById('file-input');

  if (fileInput.files.length > 0) {
    formData.set('file', fileInput.files[0]);
  } else {
    formData.delete('file');
  }

  issuesList.innerHTML = '<p>Analyzing…</p>';
  reportOutput.textContent = 'Generating report…';
  previewTableHead.innerHTML = '';
  previewTableBody.innerHTML = '';

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Request failed');
    }

    const result = await response.json();
    renderResults(result);
  } catch (error) {
    issuesList.innerHTML = '<p>Unable to analyze the dataset. Please try again.</p>';
    reportOutput.textContent = error.message;
  }
});

function renderResults(result) {
  rowCount.textContent = result.rows;
  columnCount.textContent = result.columns.length;
  issueCount.textContent = result.issue_count;
  qualityPill.textContent = `${result.quality_score}/100 quality`;

  if (result.issues.length === 0) {
    issuesList.innerHTML = '<p>No issues detected. The data looks healthy.</p>';
  } else {
    issuesList.innerHTML = result.issues
      .map((issue) => `
        <article class="issue-card">
          <div class="issue-header">
            <strong>${issue.issue_type.replace('_', ' ')}</strong>
            <span class="badge ${issue.severity}">${issue.severity}</span>
          </div>
          <p>${issue.description}</p>
          <p><strong>Recommendation:</strong> ${issue.recommendation}</p>
        </article>
      `)
      .join('');
  }

  reportOutput.textContent = result.report;

  if (result.preview_rows.length > 0) {
    const headers = Object.keys(result.preview_rows[0]);
    previewTableHead.innerHTML = `
      <tr>${headers.map((header) => `<th>${header}</th>`).join('')}</tr>
    `;
    previewTableBody.innerHTML = result.preview_rows
      .map((row) => `
        <tr>${headers.map((header) => `<td>${row[header] ?? ''}</td>`).join('')}</tr>
      `)
      .join('');
  }
}
