import { useEffect, useState } from "react";
import { checkHealth } from "../api/health";

export default function HealthPage() {
  const [status, setStatus] = useState<string>("Checking...");

  useEffect(() => {
    checkHealth().then(setStatus);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Health</h1>
      <div className={`p-3 rounded ${status === "OK" ? "bg-green-200" : "bg-red-200"}`}>
        Backend Status: {status}
      </div>
    </div>
  );
}
