export default function ApplicationTable({ data }) {
  if (!data || data.length === 0) {
    return <p className="text-slate-500">No applications found.</p>
  }

  return (
    <div className="overflow-x-auto bg-white rounded-xl border border-slate-200">
      <table className="w-full text-sm">
        <thead className="bg-slate-100 text-left">
          <tr>
            <th className="p-3">Trainer ID</th>
            <th className="p-3">Skills</th>
            <th className="p-3">Experience</th>
            <th className="p-3">Score</th>
            <th className="p-3">CV</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr className="border-t" key={row.id}>
              <td className="p-3">#{row.trainer_id}</td>
              <td className="p-3">{row.skills || '-'}</td>
              <td className="p-3">{row.years_experience} years</td>
              <td className="p-3 font-semibold">{row.relevance_score}</td>
              <td className="p-3">
                <a href={row.cv_url} target="_blank" rel="noreferrer" className="text-brand underline">
                  Open CV
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
