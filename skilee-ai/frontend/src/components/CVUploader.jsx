import { useRef, useState } from 'react'

export default function CVUploader({ onFile }) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef(null)

  const handleFile = (file) => {
    if (file) onFile(file)
  }

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer ${dragging ? 'border-brand bg-teal-50' : 'border-slate-300 bg-white'}`}
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault()
        setDragging(false)
        handleFile(e.dataTransfer.files?.[0])
      }}
    >
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".pdf"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />
      <p className="text-slate-700">Drag and drop CV (PDF) or click to upload</p>
    </div>
  )
}
