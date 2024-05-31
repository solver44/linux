import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function ClassTable() {
  const [classes, setClasses] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    axios
      .get("/api/classes")
      .then((response) => setClasses(response.data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="container">
      <button
        style={{ right: 0, top: -30, position: "absolute" }}
        className="button is-info details-row mt-3"
      >
        <Link style={{ color: "white" }} to="upload">
          Добавить новый источник
        </Link>
      </button>
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
            <th>Класс</th>
            <th>ОС</th>
            <th>Добавлена</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody className="classTable">
          {classes
            .filter(
              (classe) =>
                classe.classe.toLowerCase().includes(search) ||
                classe.os.toLowerCase().includes(search)
            )
            .map((classe) => (
              <tr key={classe.classe + classe.os}>
                <td>{classe.classe}</td>
                <td>{classe.os}</td>
                <td>{classe.date_crea}</td>
                <td>
                  <div className="buttons">
                    <button className="button is-info details-row">
                      <a
                        style={{ color: "white!important" }}
                        href={`/details?classe=${classe.classe}&os=${classe.os}`}
                      >
                        Детали
                      </a>
                    </button>
                    <button className="button is-danger delete-row">
                      Удалить
                    </button>
                  </div>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default ClassTable;
