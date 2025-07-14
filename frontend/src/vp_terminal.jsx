import React, { useState } from 'react';

const VpTerminal = () => {
  const [userId, setUserId] = useState('');
  const [orderNumber, setOrderNumber] = useState('');
  const [operationCode, setOperationCode] = useState('');
  const [operationId, setOperationId] = useState(null);
  const token = "user";

  const start = async () => {
    const res = await fetch("/start", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({ user_id: parseInt(userId), order_number: orderNumber, operation_code: operationCode })
    });
    const data = await res.json();
    setOperationId(data.operation_id);
  };

  const stop = async () => {
    if (!operationId) return;
    await fetch("/stop", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({ operation_id: operationId })
    });
    setOperationId(null);
  };

  return (
    <div style={{ fontFamily: "Arial", padding: "20px" }}>
      <h2>Odhlasovanie výrobných operácií</h2>
      <input placeholder="ID pracovníka" value={userId} onChange={e => setUserId(e.target.value)} /><br />
      <input placeholder="Výrobný príkaz" value={orderNumber} onChange={e => setOrderNumber(e.target.value)} /><br />
      <input placeholder="Kód operácie" value={operationCode} onChange={e => setOperationCode(e.target.value)} /><br />
      <button onClick={start}>START</button>
      <button onClick={stop} disabled={!operationId}>STOP</button>
    </div>
  );
};

export default VpTerminal;