// 파일 위치: pdfproject/static/script.js

document.addEventListener('DOMContentLoaded', () => {
  const jpgInput = document.getElementById('jpgFiles');
  const previewContainer = document.getElementById('preview');
  const form = document.getElementById('uploadForm');
  const downloadSection = document.getElementById('downloadSection');
  const downloadLink = document.getElementById('downloadLink');

  // 이미지 미리보기 기능
  jpgInput.addEventListener('change', () => {
    previewContainer.innerHTML = ''; // 초기화
    const files = jpgInput.files;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const reader = new FileReader();

      reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        previewContainer.appendChild(img);
      };

      reader.readAsDataURL(file);
    }
  });

  // 폼 제출 시 PDF 변환 요청
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    const response = await fetch('/convert', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      downloadLink.href = url;
      downloadSection.style.display = 'block';
    } else {
      alert('PDF 변환에 실패했습니다. 다시 시도해 주세요.');
    }
  });
});
