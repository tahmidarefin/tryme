import { useState, useEffect } from 'react'
import SingleChoice from './SingleChoice.jsx'
import MultiChoice from './MultiChoice.jsx'
import TextSubmit from './TextSubmit.jsx'
import ImageUpload from './ImageUpload.jsx'
import Modal from './Modal.jsx'
import CreateExam from './CreateExam.jsx'

export default function QuestionsList({ questions, valid, modeProp}) {
  const [data, setData] = useState(questions);
  const [formState, setFormState] = useState("");
  const [mode, setMode] = useState(modeProp);
  let examList = [];

  const getAllData = () => {
    (async () => {
      const response = await fetch('http://localhost:8000/questions');
      const _data = await response.json();
      if(_data.hasOwnProperty('questions')) {
        setData(_data.questions);
      }
      console.log(_data);
    })();
  }

  const selectQuestion = (e, value) => {
    e.preventDefault();
    if(value.hasOwnProperty("id")) {
      examList.push(value);
      e.currentTarget.style.display = 'none';
    }
  };

  const addQuestions = (e) => {
    e.preventDefault();
    (async () => {
      const response = await fetch('http://localhost:8000/questions', {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
      });
      const _data = await response.json();
      console.log(_data);
    })();
    getAllData();
  };

  const createExam = (e) => {
    e.preventDefault();
    setFormState("view");
    setMode("exam");
    setData(examList);
  }


  useEffect(() => {
    if(mode === "view") {
      getAllData();
    }
  }, []);

  return (
    <>
      <div>
        {data &&
        <form onSubmit={addQuestions}>
          {data.map((value, index) => {
            const type = value["type"];
            if(type === 'text') {
              return (<div key={index}>
              {mode !== "exam" && <button onClick={(e) => selectQuestion(e, value)} type="button">
                  <svg xmlns="http://www.w3.org/2000/svg" height="20" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
              </button>}
              <TextSubmit preview={true} item={value} id={index} />
              </div>);
            } else if(type === 'image_upload') {
              return (<div key={index}>
               {mode !== "exam" && <button onClick={(e) => selectQuestion(e, value)} type="button">
                  <svg xmlns="http://www.w3.org/2000/svg" height="20" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
              </button>}
              <ImageUpload preview={true} item={value} id={index} />
              </div>);
            } else if(type === 'single_choice') {
              return (<div key={index}>
               {mode !== "exam" && <button onClick={(e) => selectQuestion(e, value)} type="button">
                  <svg xmlns="http://www.w3.org/2000/svg" height="20" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
              </button>}
              <SingleChoice preview={true} item={value} id={index} />
              </div>);
            } else {
              return (<div key={index}>
               {mode !== "exam" && <button onClick={(e) => selectQuestion(e, value)} type="button">
                  <svg xmlns="http://www.w3.org/2000/svg" height="20" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
              </button>}
              <MultiChoice preview={true} item={value} id={index} />
              </div>);
            }
          })}
          {mode === "parse" && valid === true && <button type="submit" onClick={addQuestions}>Save</button>}
          {mode === "view" && <button type="button" onClick={createExam}>Create</button>}
        </form>}
        {formState === "view" && <CreateExam exams={data} />}
      </div>
    </>
  )
}
