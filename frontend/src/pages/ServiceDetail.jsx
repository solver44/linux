import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

function Details() {
  const [data, setData] = useState([]);
  let { id } = useParams();

  useEffect(() => {
    if(!id) return;
    axios
      .get(`/api/services/logs/` + id)
      .then((response) => setData(response.data))
      .catch((error) => console.error(error));
  }, [id]);

  return (
    <div>
      <h3 className="title is-3" style={{ textAlign: "center" }}>
        Детали {id}
      </h3>
      {data.map((d) => (
        <article
          class={"message" + (d.type === "error" ? "is-danger" : "is-dark")}
        >
          <div class="message-body">
            <strong>{d.stage}</strong>
            <br />
            {d.message}
            {d.detail && <pre>{d.detail}</pre>}
          </div>
        </article>
      ))}
    </div>
  );
}

export default Details;
