import { useState } from 'react'

import QuestionsList from './QuestionsList.jsx'

export default function ExamCreate({ exams }) {
  const [formState, setFormState] = useState("view")

  const handleSubmit = (e) => {
    e.preventDefault();
    const exam = new FormData(e.target);
    const {title, duration} = Object.fromEntries(exam.entries());
    const obj = {
      "title": title,
      "duration": duration,
      "ques_list": exams.map(value => value.id)
    }
    console.log(obj);
    (async () => {
      const response = await fetch('http://localhost:8000/exams', {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(obj)
      });
      const _data = await response.json();
      console.log(_data);
    })();
  };

  return (<>
    <form onSubmit={handleSubmit}>
      <label>Examination Name</label>
      <input type="text" name="title" />
      <label>Duration</label>
      <input type="number" name="duration" />
      <button onClick={() => setFormState("view")}>Save</button>
    </form>
    {formState === "view" && <QuestionsList modeProp={"exam"} exams={exams} />}
    </>);
}