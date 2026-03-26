import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

type Position = [number, number];

type Route = {
  id: number;
  title: string;
  description: string;
  start: { lat: string; lng: string };
  end: { lat: string; lng: string };
};

export default function Home() {
  const [routes, setRoutes] = useState<Route[]>([]);

  useEffect(() => {
    // in produzione usa il tuo backend
    fetch("http://localhost:8000/routes")
      .then((r) => r.json())
      .then(setRoutes);
  }, []);

  return (
    <main style={{ display: "flex", height: "100vh" }}>
      <div style={{ flex: 1 }}>
        <h1>Driving Social – percorsi</h1>
        <ul>
          {routes.map((r) => (
            <li key={r.id}>
              <h3>{r.title}</h3>
              <p>{r.description}</p>
            </li>
          ))}
        </ul>
      </div>
      <div style={{ flex: 2 }}>
        <MapContainer
          center={[41.9, 12.5]}
          zoom={10}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {routes.map((r) => {
            const start: Position = [
              parseFloat(r.start.lat),
              parseFloat(r.start.lng),
            ];
            const end: Position = [
              parseFloat(r.end.lat),
              parseFloat(r.end.lng),
            ];
            return (
              <Polyline positions={[start, end]} color="blue" key={r.id} />
            );
          })}
        </MapContainer>
      </div>
    </main>
  );
}
