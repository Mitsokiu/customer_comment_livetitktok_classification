const categories = [
  "Spam / Không liên quan",
  "Khen ngợi / Tương tác tích cực",
  "Hỏi thông tin sản phẩm",
  "Khẩn cấp / Cần phản hồi nhanh",
  "Hỏi vận chuyển / Thanh toán",
  "Hỏi giá",
  "Phàn nàn / Tiêu cực",
  "Chốt đơn / Mua hàng"
]

function renderChatGrid(){
  const grid = document.getElementById("chatGrid")
  grid.innerHTML = ""
  categories.forEach((cat, idx)=>{
    const box = document.createElement("div")
    box.className="chatbox"
    box.innerHTML = `
      <h3>${cat}</h3>
      <div class="messages" id="msg-${idx}"></div>
    `
    grid.appendChild(box)
  })
}

// Lấy username từ link TikTok
function getUsernameFromLink(link) {
  try {
      const url = new URL(link); // tạo object URL
      const pathname = url.pathname; // /@username/video/123456
      const match = pathname.match(/^\/@([^\/]+)/); // regex lấy username sau @
      if(match && match[1]){
          return match[1];
      }
  } catch (e) {
      console.error("Link không hợp lệ", e);
  }
  return null;
}

function loadComments(){
  const link = document.getElementById("tiktokLink").value.trim()
  if(!link){
    alert("Vui lòng nhập link TikTok!")
    return
  }

  const username = getUsernameFromLink(link);
  if(!username){
      alert("Không tìm thấy username!");
      return;
  }

  console.log("Username:", username);

  // Gửi username lên server
  fetch("/submit-username?username=" + encodeURIComponent(username), {
      method: "POST"
  })
  .then(res => res.json())
  .then(data => {
      console.log("Server trả về:", data);

      // Sau khi gửi username -> start lắng nghe comment
      fetch("/send_cmt")
        .then(r => r.json())
        .then(d => console.log("Listening:", d))

      // Bắt đầu polling lấy comment mới
      setInterval(fetchComments, 2000); // gọi API mỗi 2 giây
  })
  .catch(err => console.error(err));
}

// Lấy comment từ server và hiển thị
function fetchComments(){
  fetch("/get_comments")
    .then(res => res.json())
    .then(data => {
      if(data.comments){
        data.comments.forEach(c => {
          addMessage(c.prediction, `${c.user}: ${c.comment}`)
        })
      }
    })
    .catch(err => console.error("Lỗi khi lấy comment:", err));
}

// Thêm comment vào box tương ứng
function addMessage(categoryIndex, text){
  const msgDiv = document.getElementById(`msg-${categoryIndex}`)
  if(msgDiv){
    const el = document.createElement("div")
    el.className="msg"
    el.innerText = text
    msgDiv.appendChild(el)
    msgDiv.scrollTop = msgDiv.scrollHeight
  }
}

window.onload = renderChatGrid
