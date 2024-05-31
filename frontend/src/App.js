import React from "react";
import { HashRouter as Router, Route, Routes } from "react-router-dom";
import ClassTable from "./pages/ClassTable";
import Details from "./pages/Details";
import UploadForm from "./pages/UploadForm";
import Navbar from "./pages/Navbar";
import Services from "./pages/Services";

function App() {
  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" index element={<ClassTable />} />
          <Route path="/services" element={<Services />} />
          <Route path="/service/:id" element={<Services />} />
          <Route path="/details" element={<Details />} />
          <Route path="/upload" element={<UploadForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
