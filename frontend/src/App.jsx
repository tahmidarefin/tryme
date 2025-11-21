import { useState } from 'react'
import './App.css'
import ParseSheet from './components/ParseSheet.jsx'
import QuestionsList from './components/QuestionsList.jsx'
import ExamList from './components/ExamList.jsx'

function App() {
  const [mode, setMode] = useState("parse");
  return (
    <>
      <nav className="nav-bar">
        <span onClick={() => setMode("parse")}>Import</span>
        <span onClick={() => setMode("list")}>Questions</span>
        <span onClick={() => setMode("exam")}>Examinations</span>
      </nav>
      { mode === "parse" && <ParseSheet /> }
      { mode === "list" && <QuestionsList modeProp={"view"} /> }
      { mode === "exam" && <ExamList /> }
    </>
  )
}

export default App
