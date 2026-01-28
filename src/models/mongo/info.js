import Mongoose from "mongoose";

const { Schema } = Mongoose;

const infoSchema = new Schema({
  date: String,
  opinion: String,
});

// export const Info = Mongoose.model("opinions", infoSchema);
export const Info = Mongoose.model("Info", infoSchema, "opinions");
