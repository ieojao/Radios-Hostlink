"use client";
import { useRef, useState } from 'react';
import { FaRegCopy, FaCheckCircle } from 'react-icons/fa';

const PLAYER_EMBED_CODE = `<iframe src=\"https://player.streammaximum.com/start/index.php?servidor=cc4&porta=20059&type=shoutcast&width=1600&height=130&artworkImageWidth=70&volume=60&visualizerRandomPreset=1&artwork=https://iead.com/wp-content/uploads/2025/05/ICONE-PLAYER.png\" height=\"130\" width=\"100%\" scrolling=\"no\" style=\"border:none\"></iframe>`;

export default function EmbedPlayerModal({ show, onClose }: { show: boolean, onClose: () => void }) {
  const codeRef = useRef<HTMLTextAreaElement>(null);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (codeRef.current) {
      codeRef.current.select();
      document.execCommand('copy');
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    }
  };

  if (!show) return null;

  return (
    <div className="modal fade show d-block embed-modal-bg" tabIndex={-1}>
      <div className="modal-dialog modal-lg modal-dialog-centered animated fadeInUp">
        <div className="modal-content border-0 rounded-4 shadow-lg">
          <div className="modal-header p-4 border-0 rounded-top-4 embed-modal-header">
            <h5 className="modal-title fw-bold text-white w-100 text-center" style={{letterSpacing:1}}>INCORPORE NOSSO PLAYER</h5>
            <button type="button" className="btn-close btn-close-white position-absolute end-0 me-3 mt-2" aria-label="Fechar" onClick={onClose}></button>
          </div>
          <div className="modal-body text-center bg-dark text-white rounded-bottom-4 p-4">
            <p className="mb-3 fs-5">É assim que o Player ficará em seu site:</p>
            <div className="d-flex flex-column align-items-center justify-content-center mb-4 embed-player-preview">
              <img src="/nav-logo.png" alt="Logo" style={{width:56, height:56, borderRadius:12, marginBottom:8, boxShadow:'0 2px 12px #0004'}} />
              <div className="d-flex align-items-center bg-gradient px-4 py-3 rounded-3 shadow-sm" style={{background: 'linear-gradient(90deg, #1e3c72 0%, #2a5298 100%)'}}>
                <span className="me-3" style={{fontSize:36, color:'#fff'}}>&#9654;</span>
                <div className="text-start">
                  <div className="fw-bold text-white">NO AR <span className="text-info">Rádio Boas Novas</span></div>
                  <div className="small text-white-50">Seu player personalizado</div>
                </div>
                <span className="ms-4" style={{fontSize:28, color:'#fff'}}>&#128266;</span>
              </div>
            </div>
            <textarea
              ref={codeRef}
              className="form-control mb-3 text-monospace border-0 shadow-sm rounded-3"
              rows={3}
              value={PLAYER_EMBED_CODE}
              readOnly
              style={{ fontSize: 14, background: '#23272b', color: '#fff' }}
              onFocus={e => e.target.select()}
            />
            <button className="btn btn-info px-4 py-2 fw-bold d-flex align-items-center mx-auto" style={{fontSize:17}} onClick={handleCopy}>
              {copied ? <FaCheckCircle className="me-2" /> : <FaRegCopy className="me-2" />} {copied ? 'Copiado!' : 'Copiar código'}
            </button>
            <div className="text-muted mt-3">Aqui está o seu código HTML. Você pode copiar e colar este código dentro do seu site!</div>
          </div>
        </div>
      </div>
      <style jsx>{`
        .embed-modal-bg {
          background: rgba(30,44,70,0.85);
          z-index: 1050;
        }
        .embed-modal-header {
          background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        }
        .embed-player-preview {
          animation: fadeIn 0.7s;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
} 