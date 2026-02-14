import { useEffect, useState } from "react"
import axios from "axios"

type Prediction = {
  timestamp: string
  zip_code: number
  beds: number
  baths: number
  sqft: number
  parking: boolean
  in_unit_laundry: boolean
  pet_friendly: boolean
  utilities_included: boolean
  asking_rent: number
  fair_rent: number
  range_low: number
  range_high: number
  delta: number
  verdict: string
  top_factors: string[]
}

export default function HistoryPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([])

  useEffect(() => {
    async function fetchPredictions() {
      try {
        const res = await axios.get<{ predictions: Prediction[] }>(
          "http://127.0.0.1:8000/predictions?limit=50"
        )
        setPredictions(res.data.predictions)
      } catch (err) {
        console.error(err)
        alert("Failed to fetch predictions")
      }
    }

    fetchPredictions()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4">
      <h1 className="text-3xl font-bold mb-6 text-center">Prediction History</h1>

      <div className="overflow-x-auto">
        <table className="min-w-full bg-white shadow-md rounded-lg">
          <thead className="bg-blue-500 text-white">
            <tr>
              <th className="px-4 py-2">Timestamp</th>
              <th className="px-4 py-2">Zip</th>
              <th className="px-4 py-2">Beds</th>
              <th className="px-4 py-2">Baths</th>
              <th className="px-4 py-2">Sqft</th>
              <th className="px-4 py-2">Asking</th>
              <th className="px-4 py-2">Fair Rent</th>
              <th className="px-4 py-2">Delta</th>
              <th className="px-4 py-2">Verdict</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((p, i) => (
              <tr
                key={i}
                className={i % 2 === 0 ? "bg-gray-100" : "bg-white"}
              >
                <td className="px-4 py-2">{new Date(p.timestamp).toLocaleString()}</td>
                <td className="px-4 py-2">{p.zip_code}</td>
                <td className="px-4 py-2">{p.beds}</td>
                <td className="px-4 py-2">{p.baths}</td>
                <td className="px-4 py-2">{p.sqft}</td>
                <td className="px-4 py-2">${p.asking_rent}</td>
                <td className="px-4 py-2">${p.fair_rent}</td>
                <td className="px-4 py-2">{p.delta}</td>
                <td className="px-4 py-2">{p.verdict}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
