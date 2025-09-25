import { NavLink } from "react-router-dom";

export default function Nav() {
  return (
    <header className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex gap-4">
        <div className="font-bold">Customer Review Manager</div>
        <nav className="flex gap-3">
          <NavLink to="/reviews" className="hover:underline">Reviews</NavLink>
          <NavLink to="/analytics" className="hover:underline">Analytics</NavLink>
          <NavLink to="/search" className="hover:underline">Search</NavLink>
          <NavLink to="/health" className="hover:underline">Health</NavLink>
        </nav>
      </div>
    </header>
  );
}
