import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar is-spaced has-shadow" role="navigation" aria-label="main navigation">
      <div className="navbar-brand">
        <div className="navbar-item is-hidden-desktop navbar-center">
          <span className="icon ip-icon has-text-dark">
            <i className="fas fa-server"></i>
          </span>
          <span><a href="/proxmox-url"><strong>Proxmox URL</strong></a></span>
        </div>
        <a href='#' role="button" className="navbar-burger burger" aria-label="menu" aria-expanded="true" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div id="navbarpages" className="navbar-menu">
        <div className="navbar-start">
          <Link to="/" className="navbar-item">
            <span className="icon has-text-info">
              <i className="fas fa-home"></i>
            </span>
            <span>Главная</span>
          </Link>
          <Link to="services" className="navbar-item">
            <span className="icon has-text-info">
              <i className="fa fa-window-restore"></i>
            </span>
            <span>Сервисы</span>
          </Link>
        </div>
      </div>
      <div className="navbar-end">
        <div className="navbar-item is-hidden-touch">
          <span className="icon ip-icon has-text-dark">
            <i className="fas fa-server"></i>
          </span>
          <span><a href="http://localhost:8006">Proxmox Panel</a></span>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;