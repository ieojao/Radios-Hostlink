"use client";
import React, { useEffect, useRef, useState } from 'react';
import { AiOutlinePauseCircle, AiOutlinePlayCircle } from 'react-icons/ai';

const HomeRadio: React.FC = () => {
  const audioInput = useRef<HTMLAudioElement | null>(null);
  const [playIcon, setPlayIcon] = useState<string>('');
  const [pauseIcon, setPauseIcon] = useState<string>('d-none');
  const [radioURL, setRadioURL] = useState<string>('');
  const [radioTitle, setRadioTitle] = useState<string>('');
  const [radioDescription, setRadioDescription] = useState<string>('');

  useEffect(() => {
    // Play Radio Automatically After 1.5 Second
    const timer = setTimeout(() => {
      if (audioInput.current) {
        handleRadioPlay();
      }
    }, 1500);

    // Get Radio Streaming URL From Data Directory
    fetch('/data/radio-url.txt')
      .then((res) => res.text())
      .then(setRadioURL);

    // Get Radio Station Title From Data Directory
    fetch('/data/radio-station-title.txt')
      .then((res) => res.text())
      .then(setRadioTitle);

    // Get Radio Station Description From Data Directory
    fetch('/data/radio-station-description.txt')
      .then((res) => res.text())
      .then(setRadioDescription);

    return () => clearTimeout(timer);
  }, []);

  const handleRadioPlay = async () => {
    try {
      await audioInput.current?.play();
      setPlayIcon('d-none');
      setPauseIcon('');
    } catch (error) {
      console.log(error);
    }
  };

  const handleRadioPause = async () => {
    try {
      await audioInput.current?.pause();
      setPlayIcon('');
      setPauseIcon('d-none');
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="container">
        <div className="row">
          <div className="col-md-8 col-lg-8">
            {radioURL && (
              <audio ref={audioInput} src={radioURL} />
            )}
          </div>
        </div>
      </div>
      <div className="container">
        <div className="row">
          <div className="col align-self-center col-md-8 col-lg-8">
            <h1 className="radio-point animated slideInDown">
              <AiOutlinePlayCircle onClick={handleRadioPlay} className={playIcon + ' radio-play-pause'} />
              <AiOutlinePauseCircle onClick={handleRadioPause} className={pauseIcon + ' radio-play-pause'} />
              99.90 FM
            </h1>
            <h1 className="radio-name ml-3 animated slideInUp">{radioTitle}</h1>
            <p className="radio-des ml-3 animated slideInUp">{radioDescription}</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default HomeRadio; 