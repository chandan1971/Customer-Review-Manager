import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/appRoutes";
import Nav from "./components/NAV";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50">
        <Nav />
        <main className="container mx-auto p-4">
          <AppRoutes />
        </main>
      </div>
    </BrowserRouter>
  );
}
