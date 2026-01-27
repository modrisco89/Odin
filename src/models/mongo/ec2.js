import Mongoose from "mongoose";

const { Schema } = Mongoose;

const ec2Schema = new Schema({
  time: String,
  cpu: String,
});

export const Ec2 = Mongoose.model("Ec2", ec2Schema, "instanceStats");
