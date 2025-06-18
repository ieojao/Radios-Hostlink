"use client";
import { AiOutlineInstagram, AiOutlineTwitter } from 'react-icons/ai';
import { FiFacebook } from 'react-icons/fi';

export default function Footer() {
  return (
    <footer className="footer-animated bg-dark text-white py-4 mt-5">
      <div className="container d-flex flex-column flex-md-row justify-content-between align-items-center">
        <div className="mb-3 mb-md-0 animated fadeInLeft">
          <span className="fw-bold">Single Internet Radio Station</span> &copy; {new Date().getFullYear()}
        </div>
        <div className="animated fadeInUp">
          <a href="#" className="text-white mx-2 fs-4 footer-social" aria-label="Facebook"><FiFacebook /></a>
          <a href="#" className="text-white mx-2 fs-4 footer-social" aria-label="Twitter"><AiOutlineTwitter /></a>
          <a href="#" className="text-white mx-2 fs-4 footer-social" aria-label="Instagram"><AiOutlineInstagram /></a>
        </div>
      </div>
      <style jsx>{`
        .footer-animated {
          background: linear-gradient(90deg, #232526 0%, #414345 100%);
          box-shadow: 0 -2px 16px rgba(0,0,0,0.2);
          animation: fadeInFooter 1.2s ease;
        }
        .footer-social {
          transition: transform 0.2s, color 0.2s;
        }
        .footer-social:hover {
          color: #ffb347 !important;
          transform: scale(1.2) rotate(-8deg);
        }
        @keyframes fadeInFooter {
          from { opacity: 0; transform: translateY(40px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </footer>
  );
} 