// 選擇檔案後顯示在 uploaded-image
document.getElementById('file-input').addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  const uploadedImage = document.getElementById('uploaded-image');
  const processedImage = document.getElementById('processed-image');
  const finalImage = document.getElementById('final-image');

  // 如果找到了 final-image 元素，則進行清除操作
  if (finalImage) {

      // 隐藏 final-image 圖片
      finalImage.style.display = 'none';

      if (finalImage) {
        // 移除 final-image 元素
        finalImage.remove();
      }
      
  }

  
  reader.onload = function(e) {
      uploadedImage.src = e.target.result;
      document.getElementById('uploaded-image').style.display = 'none';//隱藏上次偵測的結果
      uploadedImage.style.display = 'block';
      processedImage.style.display = 'none'; // 隱藏處理後的圖片
  };

  reader.readAsDataURL(file);
});

// 上傳圖片並顯示在 processed-image
function uploadImage() {
  const fileInput = document.getElementById('file-input');
  const processedImage = document.getElementById('processed-image');

  // 檢查是否選擇了檔案
  if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append('file', file);

      // 上傳圖片到伺服器並處理
      fetch('/upload', {
          method: 'POST',
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          // 獲取圖片資料
          const imageData = data.image;

          // 創建圖片元素
          const img = document.createElement('img');
          
          // 設置上傳的圖片的 ID 
          img.id = 'final-image';

          // 設定圖片的 src 属性為接收到的 Base64 編碼的圖片數據
          img.src = imageData;

          // 將圖片添加到頁面中
          document.getElementById('image-container').appendChild(img);

          
          processedImage.src = 'data:image/jpeg;base64,' + data.image;
          document.getElementById('uploaded-image').style.display = 'none'; // 隱藏上傳的圖片
          
      })
      .catch(error => console.error('Error:', error));
  } else {
      console.error('No file selected.');
  }
}

