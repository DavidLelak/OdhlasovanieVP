import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function AdminUserPanel() {
  const [users, setUsers] = useState([]);
  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const fetchUsers = async () => {
    const res = await axios.get("/api/users");
    setUsers(res.data);
  };

  const addUser = async () => {
    await axios.post("/api/users", {
      username: newUsername,
      password: newPassword,
    });
    setNewUsername("");
    setNewPassword("");
    fetchUsers();
  };

  const deleteUser = async (id) => {
    await axios.delete(`/api/users/${id}`);
    fetchUsers();
  };

  const toggleActive = async (id, active) => {
    await axios.patch(`/api/users/${id}`, { active: !active });
    fetchUsers();
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Správa používateľov</h1>

      <div className="mb-4 space-x-2">
        <Input
          placeholder="Používateľské meno"
          value={newUsername}
          onChange={(e) => setNewUsername(e.target.value)}
        />
        <Input
          type="password"
          placeholder="Heslo"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
        <Button onClick={addUser}>Pridať používateľa</Button>
      </div>

      <div className="grid gap-4">
        {users.map((user) => (
          <Card key={user.id}>
            <CardContent className="flex items-center justify-between p-4">
              <div>
                <p className="font-semibold">{user.username}</p>
                <p className="text-sm text-gray-500">Rola: {user.role}</p>
                <p className="text-sm text-gray-500">
                  Stav: {user.active ? "Aktívny" : "Neaktívny"}
                </p>
              </div>
              <div className="space-x-2">
                <Button onClick={() => toggleActive(user.id, user.active)}>
                  {user.active ? "Deaktivovať" : "Aktivovať"}
                </Button>
                <Button variant="destructive" onClick={() => deleteUser(user.id)}>
                  Zmazať
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
