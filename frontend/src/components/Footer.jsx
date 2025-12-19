import { Shield, ExternalLink } from "lucide-react";
import { Link } from "react-router-dom";
import "./Footer.css"; // important

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">

        {/* Bloc 1 : Logo & Description */}
        <div className="footer-block">
          <div className="footer-brand">
            <div className="footer-logo">
              <Shield className="footer-logo-icon" />
            </div>
            <span className="footer-title">
              Nahj<span className="footer-yellow">Tribunal</span> Monitor
            </span>
          </div>

          <p className="footer-text">
            Urban crime information and analysis tool. Data
            from Chicago Open Data, stored in MongoDB, indexed via
            Elasticsearch and visualized with Kibana.
          </p>
        </div>

        {/* Bloc 2 : Navigation */}
        <div className="footer-block">
          <h4 className="footer-heading">Navigation</h4>
          <ul className="footer-list">
            <li><Link to="/" className="footer-link">Home</Link></li>
            <li><Link to="/explorer" className="footer-link">Crime Explorer</Link></li>
            <li><Link to="/analytics" className="footer-link">Analytics</Link></li>
            <li>
  <span
    className="footer-link"
    style={{ cursor: "pointer" }}
    onClick={() => {
      window.location.href = "/#features";
    }}
  >
    About Us
  </span>
</li>

          </ul>
        </div>

        {/* Bloc 3 : Ressources */}
        <div className="footer-block">
          <h4 className="footer-heading">Ressources</h4>
          <ul className="footer-list">
            <li>
              <a href="https://data.cityofchicago.org/" target="_blank" rel="noopener noreferrer" className="footer-link">
                Open Data Chicago <ExternalLink className="footer-ext-icon" />
              </a>
            </li>
            <li>
              <a href="#" className="footer-link">
                Documentation API <ExternalLink className="footer-ext-icon" />
              </a>
            </li>
          </ul>
        </div>
      </div>

      {/* Ligne du bas */}
      <div className="footer-bottom">
        <p>© 2025 Nahj Tribunal Monitor. Educational project.</p>
        <p>This site does not provide legal advice or emergency assistance.</p>
      </div>
    </footer>
  );
};

export default Footer;
