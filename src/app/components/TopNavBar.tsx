"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { AiOutlineInstagram, AiOutlineTwitter } from 'react-icons/ai';
import { FiFacebook } from 'react-icons/fi';
import EmbedPlayerModal from './EmbedPlayerModal';

const TopNavBar: React.FC = () => {
  const [facebookLink, setFacebookLink] = useState('');
  const [twitterLink, setTwitterLink] = useState('');
  const [instagramLink, setInstagramLink] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetch('/data/facebook-link.txt').then(res => res.text()).then(setFacebookLink);
    fetch('/data/twitter-link.txt').then(res => res.text()).then(setTwitterLink);
    fetch('/data/instagram-link.txt').then(res => res.text()).then(setInstagramLink);
  }, []);

  return (
    <>
      <nav className="navbar navbar-dark navbar-expand-lg">
        <div className="container">
          <Link className="nav-link" href="/">
            <Image alt="nav-logo" className="nav-logo" src="/nav-logo.png" width={40} height={40} />
          </Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#basic-navbar-nav" aria-controls="basic-navbar-nav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="basic-navbar-nav">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <Link className="nav-link" href="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/about">About</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/schedule">Schedule</Link>
              </li>
            </ul>
            <div className="d-flex align-items-center">
              <a target="_blank" rel="noopener noreferrer" className="nav-link-social" href={facebookLink}><FiFacebook /></a>
              <a target="_blank" rel="noopener noreferrer" className="nav-link-social" href={twitterLink}><AiOutlineTwitter /></a>
              <a target="_blank" rel="noopener noreferrer" className="nav-link-social" href={instagramLink}><AiOutlineInstagram /></a>
              <button className="btn btn-outline-info ms-3" style={{whiteSpace:'nowrap'}} onClick={() => setShowModal(true)}>
                Incorpore o Player
              </button>
            </div>
          </div>
        </div>
      </nav>
      <EmbedPlayerModal show={showModal} onClose={() => setShowModal(false)} />
    </>
  );
};

export default TopNavBar; 