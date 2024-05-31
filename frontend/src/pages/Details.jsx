import React, { useState, useEffect } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";

function Details() {
  const [students, setStudents] = useState([]);
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const classe = params.get("classe");
  const os = params.get("os");

  useEffect(() => {
    axios
      .get(`/api/details?classe=${classe}&os=${os}`)
      .then((response) => setStudents(response.data))
      .catch((error) => console.error(error));
  }, [classe, os]);

  return (
    <div>
      <h3 className="title is-3" style={{ textAlign: "center" }}>
        Детали {classe} {os}
      </h3>
      <table className="table" style={{ margin: "auto" }}>
        <thead>
          <tr>
            <th>Vmid</th>
            <th>Узел</th>
            <th>Имя</th>
            <th>Фамилия</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.id_vm}>
              <td>{student.id_vm}</td>
              <td>{student.node}</td>
              <td>{student.firstname}</td>
              <td>{student.lastname}</td>
              <td>{student.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Details;
