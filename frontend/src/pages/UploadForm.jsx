import React, { useState } from "react";
import axios from "axios";
import { HTTPRequests } from "../config";

function UploadForm() {
  const [selectedRequest, setRequest] = useState("default");
  const [selectedOS, setSelectedOS] = useState("alpine");
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [name, setName] = useState("");
  const [interval, setInterval] = useState(10);
  const [startAfterCreation, setStartAfterCreation] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleUpload = () => {
    setLoading(true);
    const formData = new FormData();
    // formData.append("file", file);
    formData.append("os", selectedOS);
    formData.append("request", selectedRequest);
    formData.append("url", url);
    formData.append("name", name);
    formData.append("interval", interval);
    formData.append("startAfterCreation", startAfterCreation);

    axios
      .post("/create", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("Upload successful:", response);
        // Handle successful upload
      })
      .catch((error) => {
        console.error("Upload error:", error);
        // Handle upload error
      });
  };

  return (
    <React.Fragment>
      <div className="box container" style={{ marginTop: 50 }}>
        <h3 className="title" style={{ textAlign: "center" }}>
          Добавить новый источник
        </h3>
        <div class="tabs">
          <ul>
            <li class="is-active">
              <a>HTTP API</a>
            </li>
            <li>
              <a>FTP</a>
            </li>
          </ul>
        </div>
        <div className="field">
          <label className="label">Имя</label>
          <div className="control">
            <input
              className="input"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Введите имя"
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Тип запроса</label>
          <div className="control has-icons-left">
            <div className="select">
              <select
                value={selectedRequest}
                onChange={(e) => setRequest(e.target.value)}
                className="select-class"
              >
                {HTTPRequests.map((h) => {
                  return (
                    <option key={h} value={h}>
                      {h}
                    </option>
                  );
                })}
              </select>
            </div>
            <div className="icon is-medium is-left">
              <i className="fas fa-graduation-cap"></i>
            </div>
          </div>
        </div>
        <div className="field">
          <label className="label">OS *</label>
          <div className="control has-icons-left">
            <div className="select">
              <select
                value={selectedOS}
                onChange={(e) => setSelectedOS(e.target.value)}
                className="select-os"
              >
                <option value="alpine">Alpine</option>
              </select>
            </div>
            <div className="icon is-medium is-left">
              <i className="far fa-window-restore"></i>
            </div>
          </div>
          {/* <p className="help is-danger">Обязательно</p> */}
        </div>

        <div className="field">
          <label className="label">URL</label>
          <div className="control">
            <input
              className="input"
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Введите URL"
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Интервал получения</label>
          <div className="select">
            <select
              className="select"
              value={interval}
              onChange={(e) => setInterval(e.target.value)}
              placeholder="Интервал"
            >
              <option value="timedelta(weeks=2)">Каждые 2 недели</option>
              <option value="timedelta(days=3)">Каждые 3 дня</option>
              <option value="timedelta(days=2)">Каждые 2 дня</option>
              <option value="timedelta(days=1, hours=12)">
                Каждые 1.5 дня
              </option>
              <option value="@daily">Каждый день</option>
              <option value="@hourly">Каждый час</option>
              <option value="timedelta(hours=6)">Каждые 6 часов</option>
              <option value="timedelta(hours=2)">Каждые 2 часа</option>
              <option value="timedelta(hours=3)">Каждые 3 часа</option>
              <option value="timedelta(weeks=1)">Каждую неделю</option>
              <option value="timedelta(minutes=30)">Каждые 30 минут</option>
              <option value="timedelta(minutes=15)">Каждые 15 минут</option>
              <option value="custom">Другой (укажите ниже)</option>
            </select>
          </div>
        </div>
        <div className="field">
          <label className="checkbox">
            <input
              type="checkbox"
              style={{ width: "auto", marginRight: 10 }}
              checked={startAfterCreation}
              onChange={(e) => setStartAfterCreation(e.target.checked)}
            />
            <span>Запустить после создания</span>
          </label>
        </div>
        {/* <div className="field">
          <label className="label">Файл .csv</label>
          <div className="file">
            <label className="file-label">
              <input
                className="file-input"
                type="file"
                name="resume"
                onChange={(e) => setFile(e.target.files[0])}
              />
              <span className="file-cta">
                <span className="file-icon">
                  <i className="fas fa-upload"></i>
                </span>
                <span className="file-label">Загрузить .csv</span>
              </span>
            </label>
          </div>
        </div> */}
        <div className="field is-grouped is-grouped-centered">
          <div className="control">
            <button
              onClick={handleUpload}
              className={"button is-link" + (loading ? "is-loading" : "")}
            >
              <strong>Сгенерировать</strong>
            </button>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
}

export default UploadForm;
