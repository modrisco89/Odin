import Mongoose from "mongoose";
import { Ec2 } from "./ec2.js";
import { infoMongoStore } from "./info-mongo-store.js";
import { Info } from "./info.js";


export const ec2MongoStore = {
  async getAllEc2s() {
    const ec2s = await Ec2.find().lean();
    return ec2s;
  },

  async getec2ById(id) {
    if (Mongoose.isValidObjectId(id)) {
      const ec2 = await Ec2.findOne({ _id: id }).lean();
      if (ec2) {
        ec2.infos = await infoMongoStore.getinfosByec2Id(ec2._id);
      }
      return ec2;
    }
    return null;
  },

  async addec2(ec2) {
    const newec2 = new Ec2(ec2);
    const ec2Obj = await newec2.save();
    return this.getec2ById(ec2Obj._id);
  },

  async getUserec2s(id) {
    const ec2 = await Ec2.find({ userid: id }).lean();
    return ec2;
  },

  async deleteec2ById(id) {
    try {
      await Ec2.deleteOne({ _id: id });
      await Info.deleteMany({ec2id: id});
    } catch (error) {
      console.log("bad id");
    }
  },

  async deleteAllec2sByUserId(id) {
    try {
      await Ec2.deleteMany({ userid: id });
      await Info.deleteMany({userid: id});
    } catch (error) {
      console.log("bad id");
    }
  },

  async deleteAllec2s() {
    await Ec2.deleteMany({});
  },
};
