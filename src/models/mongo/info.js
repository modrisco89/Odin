import Mongoose from "mongoose";

const { Schema } = Mongoose;

const infoSchema = new Schema({
  artist: String,
  price: Number,
  date: String,
  genre: String,
  venueid: {
    type: Schema.Types.ObjectId,
    ref: "venue",
  },
  userid: {
    type: Schema.Types.ObjectId,
    ref: "User",
  },
});

// export const Info = Mongoose.model("opinions", infoSchema);
export const Info = Mongoose.model("Info", infoSchema, "opinions");
