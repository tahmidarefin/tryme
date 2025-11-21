import { useState, useEffect } from 'react'

export default function ExamList() {
  const [data, setData] = useState(null);

  const getAllData = () => {
    (async () => {
      const response = await fetch('http://localhost:8000/exams');
      const _data = await response.json();
      if(_data.hasOwnProperty('examinations')) {
        setData(_data.examinations);
      }
    })();
  }

  useEffect(() => {
    getAllData();
  }, []);

  return (
    <>
      <div>
        { data && data.map((value, index) => {
          return (<li key={index}>
            {value.title} {value.duration} mints
          </li>);
        }) }
      </div>
    </>
  )
}
