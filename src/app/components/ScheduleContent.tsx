"use client";

import React, { useEffect, useState } from 'react';

const ScheduleContent: React.FC = () => {
  const [content, setContent] = useState('');

  useEffect(() => {
    fetch('/data/schedule.txt')
      .then((res) => res.text())
      .then(setContent);
  }, []);

  return (
    <div className="container-fluid my-5">
      <div className="row d-flex justify-content-center">
        <div className="col-md-10 col-sm-10 col-lg-10 col-12">
          <div className="card animated fadeIn">
            <div className="card-body">
              <div className="animated fadeIn" dangerouslySetInnerHTML={{ __html: content }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScheduleContent; 