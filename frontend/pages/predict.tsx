import { useState } from "react"
import axios from "axios"

// Define the TypeScript type for the form inputs
type PredictForm = {
  zip_code: number
  beds: number
  baths: number
  sqft: number
  parking: boolean
  in_unit_laundry: boolean
  pet_friendly: boolean
  utilities_included: boolean
  asking_rent: number
}

// Define the TypeScript type for the prediction response
type PredictResponse = {
  fair_rent: number
  range_low: number
  range_high: number
  delta: number
  verdict: string
  top_factors: string[]
}

export default function PredictPage() {
  // Form state
  const [form, setForm] = useState<PredictForm>({
    zip_code: 53703,
    beds: 1,
    baths: 1,
    sqft: 500,
    parking: false,
    in_unit_laundry: false,
    pet_friendly: false,
    utilities_included: false,
    asking_rent: 1000,
  })

  // State to store prediction
  const [prediction, setPrediction] = useState<PredictResponse | null>(null)

  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : Number(value),
    })
  }

  // Submit form
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await axios.post<PredictResponse>(
        "http://127.0.0.1:8000/predict",
        form
      )
      setPrediction(res.data)
    } catch (err) {
      console.error(err)
      alert("Prediction failed")
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Madison Rent Deal Detector</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Zip Code:</label>
          <input
            type="number"
            name="zip_code"
            value={form.zip_code}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Beds:</label>
          <input
            type="number"
            name="beds"
            value={form.beds}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Baths:</label>
          <input
            type="number"
            step="0.5"
            name="baths"
            value={form.baths}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Sqft:</label>
          <input
            type="number"
            name="sqft"
            value={form.sqft}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Parking:</label>
          <input
            type="checkbox"
            name="parking"
            checked={form.parking}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>In-Unit Laundry:</label>
          <input
            type="checkbox"
            name="in_unit_laundry"
            checked={form.in_unit_laundry}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Pet Friendly:</label>
          <input
            type="checkbox"
            name="pet_friendly"
            checked={form.pet_friendly}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Utilities Included:</label>
          <input
            type="checkbox"
            name="utilities_included"
            checked={form.utilities_included}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Asking Rent:</label>
          <input
            type="number"
            name="asking_rent"
            value={form.asking_rent}
            onChange={handleChange}
          />
        </div>

        <button type="submit">Predict</button>
      </form>

      {prediction && (
        <div style={{ marginTop: 20 }}>
          <h2>Prediction Result</h2>
          <p>Fair Rent: ${prediction.fair_rent}</p>
          <p>Range: ${prediction.range_low} - ${prediction.range_high}</p>
          <p>Delta: ${prediction.delta}</p>
          <p>Verdict: {prediction.verdict}</p>
          <p>Top Factors:</p>
          <ul>
            {prediction.top_factors.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
