import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function Services() {
  const [data, setData] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    axios
      .get("/api/services/instances")
      .then((response) => setData(response.data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="container">
      <h3 className="title mt-6" style={{ textAlign: "center" }}>
        Список
      </h3>
      <div className="columns is-centered">
        <div className="column is-4">
          <div className="field">
            <p className="control has-icons-left has-icons-right">
              <input
                className="input"
                type="text"
                placeholder="Поиск"
                value={search}
                onChange={(e) => setSearch(e.target.value.toLowerCase())}
              />
              <span className="icon is-small is-left">
                <i className="fas fa-search"></i>
              </span>
            </p>
          </div>
        </div>
      </div>
      <table className="table" id="table-class" style={{ margin: "auto" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Запущена</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody className="classTable">
          {data
            .filter(
              (classe) =>
                classe.classe.toLowerCase().includes(search) ||
                classe.os.toLowerCase().includes(search)
            )
            .map((id) => (
              <tr key={id}>
                <td>
                  <Link to={"/service/" + id}>{id}</Link>
                </td>
                <td></td>
                <td></td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default Services;
