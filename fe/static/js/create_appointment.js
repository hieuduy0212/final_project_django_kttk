function showLoading(s) {
  if (s) {
    document.getElementById("overlay").style.display = "flex";
    document.getElementById("loading").style.display = "block";
  } else {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("loading").style.display = "none";
  }
}
async function getDoctor() {
  showLoading(true);
  let doctor_url = "http://localhost:8001/doctor/api/doctors/";

  const response = await fetch(doctor_url, {
    method: "GET",
  });

  const data = await response.json();

  let content = ``;
  if (data.length != 0) {
    const doctorSelect = document.getElementById("doctor_id_select");
    doctorSelect.innerHTML = `<option value="" disabled selected>Chọn bác sĩ</option>`;
    console.log(data);
    data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = `${item.full_name.first_name} ${item.full_name.mid_name} ${item.full_name.last_name}`;
        doctorSelect.appendChild(option);
    });
  } else {
    document.getElementById("doctor_id_select").innerText =  'Chưa có bác sĩ nào';
  }
  showLoading(false);
}
getDoctor();

async function getRoom() {
  showLoading(true);
  let room_url = "http://localhost:8003/room_bed/api/rooms/";

  const response = await fetch(room_url, {
    method: "GET",
  });

  const data = await response.json();

  if (data.length != 0) {
    const doctorSelect = document.getElementById("room_id_select");
    doctorSelect.innerHTML = `<option value="" disabled selected>Chọn phòng</option>`;
    console.log(data);
    data.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = `${item.room_number}`;
      doctorSelect.appendChild(option);
    });
  } else {
    document.getElementById("doctor_id_select").innerText =
      "Chưa có bác sĩ nào";
  }
  showLoading(false);
}
getRoom();

async function getPatient() {
  showLoading(true);
  let room_url = "http://localhost:8002/patients/api/patients/";

  const response = await fetch(room_url, {
    method: "GET",
  });

  const data = await response.json();

  if (data.length != 0) {
    const doctorSelect = document.getElementById("patient_id_select");
    doctorSelect.innerHTML = `<option value="" disabled selected>Chọn bệnh nhân</option>`;
    console.log(data);
    data.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = `${item.full_name.first_name} ${item.full_name.mid_name} ${item.full_name.last_name} - ${item.tel} - ${item.address.no_house} ${item.address.street} ${item.address.city}`;
      doctorSelect.appendChild(option);
    });
  } else {
    document.getElementById("patient_id_select").innerText =
      "Chưa có bác sĩ nào";
  }
  showLoading(false);
}
getPatient();
const createAppointmentForm = document.getElementById("create_appointment_form");
createAppointmentForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const patient_id = document.getElementById("patient_id_select").value;
  const hour = document.getElementById("hour").value;
  const visit_date = document.getElementById("visit_date").value;
  const reason = document.getElementById("reason").value;
  const doctor_id = document.getElementById("doctor_id_select").value;
  const room_id = document.getElementById("room_id_select").value;

  const appointmentData = {
    patient_id: patient_id,
    hour: hour,
    visit_date: visit_date,
    reason: reason,
    doctor_id: doctor_id,
    room_id: room_id,
    appointment_date: getCurrentDate(),
  };
  console.log(JSON.stringify(appointmentData));


  fetch("http://localhost:8004/appointments/api/appointments/create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(appointmentData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      alert("Đặt lịch thành công");
      window.location.href = "http://localhost:8000/list-appointment"
    })
    .catch((error) => {
      console.error("Error:", error);
      // Xử lý lỗi ở đây (ví dụ: hiển thị thông báo lỗi, ...)
    });
})

function getCurrentDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Tháng tính từ 0, nên cần +1 và đảm bảo định dạng 2 chữ số
    const day = String(today.getDate()).padStart(2, '0'); // Đảm bảo định dạng 2 chữ số

    return `${year}-${month}-${day}`;
}
