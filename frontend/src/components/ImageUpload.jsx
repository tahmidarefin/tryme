import { useState } from 'react'

export default function ImageUpload({item, id}) {
    const [img, setImg] = useState(null);

    const [data, setData] = useState(item);

    const deleteQuestion = (e) => {
        e.preventDefault();
        (async () => {
            const response = await fetch(`http://localhost:8000/questions/${item.id}`, {
                method: "DELETE",
            });
            const _data = await response.json();
            console.log(_data);
            setData({});
        })();
    }

    if(!item.hasOwnProperty('id')) {
        item["id"] = id;
    }
    const [file, setFile] = useState(null);
    const handleChange = (e) => {
        e.preventDefault();
        setImg(e.target.files[0])
    }

    const handleUpload = (e) => {
        e.preventDefault();
        setFile(URL.createObjectURL(img));
        const _data = new FormData();
        _data.append("file", img, `11_${item.id}.${img.name.split('.').pop()}`); // key, value, new_name
        (async () => {
            const response = await fetch('http://localhost:8000/upload', {
                method: "POST",
                body: _data
            });
            const data = await response.json();
            console.log(data);
        })();
    }

    return (
        <>
        { data.hasOwnProperty('id') &&
        <div className="question">
            <div className="question-op">
                <p className="title">{data["title"]}</p>
                <button onClick={deleteQuestion}>
                    <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" >
                        <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                </button>
            </div>
            <div className="info">
                <span>Class {data["complexity"]}</span>
                <span>Long Answer</span>
                <span>Score: {data["max_score"]}</span> 
            </div>
            <div className="answer">
                <div className="image">
                    <input type="file" id={`${data["id"]}`} onChange={handleChange} name={`${data["id"]}`} accept=".jpg" />
                    <button onClick={handleUpload} type="button">Upload</button>
                </div>
                <div>
                    { file && <img src={file} alt="preview" width="200" />}
                </div>
            </div>
        </div> }
        </>
    );
}