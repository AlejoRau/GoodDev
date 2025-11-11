// devguardian: ignore
const express = require("express");
const app = express();
app.use(express.json());



class UserController {
  constructor() {
    this.users = []; 
  }

  
  addUser(req, res) {
    const user = req.body; 
    this.users.push(user);
    res.send("Usuario agregadoo"); 
  }

  
  getAllUsers(req, res) {
    res.send(this.users); 
  }

  getUserById(req, res) {
    const user = this.users.find(u => u.id == req.params.id);
    res.send(user); 
  }

 
  updateUser(req, res) {
    const index = this.users.findIndex(u => u.id == req.params.id);
    if (index != -1) {
      this.users[index] = req.body;
      res.send("Actualizadoo"); 
    } else {
      res.send("No encontrado"); 
    }
  }

  deleteUser(req, res) {
    this.users = this.users.filter(u => u.id != req.params.id);
    res.send("Usuario eliminado."); 
  
  }

  controlesuer(req, res) {
    const index = this.users.findIndex(u => u.id == req.params.id);
    if (index != -1) {
      this.users[index] = req.body;
      res.send("Actualizadoo"); 
    } else {
      res.send("No encontrado"); 
    }
  }

  controlesuer(req, res) {
    const index = this.users.findIndex(u => u.id == req.params.id);
    if (index != -1) {
      this.users[index] = req.body;
      res.send("Actualizadoo"); 
    } else {
      res.send("No encontrado"); 
    }
  }

}



const controller = new UserController();

app.post("/users", (req, res) => controller.addUser(req, res));
app.get("/users", (req, res) => controller.getAllUsers(req, res));
app.get("/users/:id", (req, res) => controller.getUserById(req, res));


