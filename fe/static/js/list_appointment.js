function showLoading(s) {
  if (s) {
    document.getElementById("overlay").style.display = "flex";
    document.getElementById("loading").style.display = "block";
  } else {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("loading").style.display = "none";
  }
}
async function getPatient() {
  showLoading(true);
  let room_url = "http://localhost:8004/appointments/api/appointments/";

  const response = await fetch(room_url, {
    method: "GET",
  });

  const data = await response.json();

  if (data.length != 0) {
    console.log(data);
    data.forEach((item) => {
      const tableBody = document
      .getElementById("appointmentTable")
      .getElementsByTagName("tbody")[0];
      tableBody.innerHTML = ""; // Clear any existing rows
      data.forEach((appointment) => {
      const row = tableBody.insertRow();
      const cellId = row.insertCell(0);
      const cellPatient = row.insertCell(1);
      const cellDoctor = row.insertCell(2);
      const cellHour = row.insertCell(3);
      const cellVisitDate = row.insertCell(4);
      const cellRoom = row.insertCell(5);
      const cellNote = row.insertCell(6);
      const a = appointment;
      cellId.textContent = appointment.id;
      cellPatient.textContent = `${a.patient.full_name.first_name} ${a.patient.full_name.mid_name} ${a.patient.full_name.last_name}`;
      cellDoctor.textContent = `${a.doctor.full_name.first_name} ${a.doctor.full_name.mid_name} ${a.doctor.full_name.last_name}`;
      cellHour.textContent = appointment.hour;
      cellVisitDate.textContent = appointment.visit_date;
      cellRoom.textContent = appointment.room_id;
      cellNote.textContent = appointment.reason;
      });
    });
  } else {
  }
  showLoading(false);
}
getPatient();
