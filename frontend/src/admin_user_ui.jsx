import React, { useEffect, useState } from 'react';

const AdminUI = () => {
  const [users, setUsers] = useState([]);
  const token = "admin";

  const fetchUsers = async () => {
    const res = await fetch("/api/users", {
      headers: { "Authorization": "Bearer " + token }
    });
    const data = await res.json();
    setUsers(data);
  };

  const deleteUser = async (id) => {
    await fetch("/api/users/" + id, {
      method: "DELETE",
      headers: { "Authorization": "Bearer " + token }
    });
    fetchUsers();
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ fontFamily: "Arial", padding: "20px" }}>
      <h1>Správa používateľov (admin)</h1>
      <ul>
        {users.map(u => (
          <li key={u.id}>
            {u.username} ({u.role}) [{u.is_active ? "✔ aktívny" : "✖ neaktívny"}]
            <button onClick={() => deleteUser(u.id)} style={{ marginLeft: "10px" }}>
              Zmazať
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminUI;