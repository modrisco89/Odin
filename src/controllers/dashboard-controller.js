import dayjs from "dayjs";
import { createRequire } from "module";
import { venueSpec } from "../models/joi-schemas.js";
import { imageStore } from "../models/image-store.js";
import { db } from "../models/db.js";

const require = createRequire(import.meta.url);
let count=0;
let flag = false;
export const dashboardController = {
  index: {
    handler: async function (request, h) {
      const loggedInUser = request.auth.credentials;
      const adminInfo = await db.adminStore.getAlladmins();
      const ec2s = await db.ec2Store.getAllEc2s();
      const opinions = await db.infoStore.getAllinfos();      
      const uptimes = ec2s
      const mems = ec2s
      const cpus = ec2s
      const stors = ec2s
      const lastUptime = uptimes.pop().uptime;
      const lastUptimeSliced = lastUptime.slice(3, lastUptime.length);
      const lastMemory = mems.pop().memUsed;
      const numlastMemory = Number(lastMemory.slice(0, 5));
      const freeMemory = 100 - numlastMemory;
      const lastStor = stors.pop().storUsed;
      const numlastStor = Number(lastStor.slice(0, 2));
      const freeStor = 100 - numlastStor;
      const lastOpinion = opinions.pop()?.opinion;
      const lastOpinionDate = opinions.pop()?.date;
      const rebootRequired = opinions.pop()?.rebootRequired;
      if (cpus.pop().CPU === "100"){
        count += 1;
      }
      else{
        count = 0;
        flag = false;
      }
      if (count > 10){
        flag = true;
      }

      const viewData = {
        title: "Odin Dashboard",
        user: loggedInUser,
        adminInfo: adminInfo,
        ec2s: ec2s,
        uptime: lastUptimeSliced,
        memory: lastMemory,
        freeMemory: freeMemory,
        usedMemory: numlastMemory,
        freeStor: freeStor,
        usedStor: numlastStor,
        opinion: lastOpinion,
        opinionDate: lastOpinionDate,
        rebootRequired: rebootRequired,
        flag: flag,
      };
      return h.view("dashboard-view", viewData);
    },
  },

  addvenue: {

    handler: async function (request, h) {
      const loggedInUser = request.auth.credentials;
      const file = request.payload.imagefile;
      const utc = require("dayjs/plugin/utc");
      const timezone = require("dayjs/plugin/timezone");
      const customParseFormat = require("dayjs/plugin/customParseFormat");
      dayjs.extend(utc);
      dayjs.extend(timezone);
      dayjs.extend(customParseFormat);
      const dateTime = dayjs();

      let url = "";
      let publicId = "";

      if (Object.keys(file).length > 0) {
            
      
      url = await imageStore.uploadImage(file);
      const reversedUrl = url.split("/").reverse().join("/");
      const publicIdWithExtension = reversedUrl.split("/")[0];
      // eslint-disable-next-line prefer-destructuring
      publicId = publicIdWithExtension.split(".")[0];
    
    }else {
      url = "https://res.cloudinary.com/dh7gl6628/image/upload/v1742276107/placeholder_zbjk5v.jpg";
      publicId = "placeholder_zbjk5v"; 
    }
      const newvenue = {
        userid: loggedInUser._id,
        title: request.payload.title,
        description: request.payload.description,
        latitude: Number(request.payload.latitude),
        longitude: Number(request.payload.longitude),
        capacity: request.payload.capacity,
        img: url,
        imgId: publicId,
      }
      const admin ={
        firstName: loggedInUser.firstName,
        email: loggedInUser.email,
        lastName: loggedInUser.lastName,
        action: "Venue Added",
        date:  dateTime.tz("Europe/London").format("DD-MM-YYYY HH:mm:ss"),
      }
      await db.adminStore.addadmin(admin);
      await db.venueStore.addvenue(newvenue);
      return h.redirect("/dashboard");
    },

    payload: {
      multipart: true,
      output: "data",
      maxBytes: 209715200,
      parse: true,
    },

    validate: {
      payload:
        venueSpec,
      options: { abortEarly: false },
      failAction: function (request, h, error) {
        return h.view("dashboard-view", { title: "Add venue error", errors: error.details }).takeover().code(400);
      },
    },
  },

  deletevenue: {
    handler: async function (request, h) {
      const venue = await db.venueStore.getvenueById(request.params.id);
      const loggedInUser = request.auth.credentials;
      const utc = require("dayjs/plugin/utc");
      const timezone = require("dayjs/plugin/timezone");
      const customParseFormat = require("dayjs/plugin/customParseFormat");
      dayjs.extend(utc);
      dayjs.extend(timezone);
      dayjs.extend(customParseFormat);
      const dateTime = dayjs();
      const admin ={
        firstName: loggedInUser.firstName,
        email: loggedInUser.email,
        lastName: loggedInUser.lastName,
        action: "Venue Deleted",
        date:  dateTime.tz("Europe/London").format("DD-MM-YYYY HH:mm:ss"),
      }
      await db.adminStore.addadmin(admin);
      await db.venueStore.deletevenueById(venue._id);
      if (venue.imgId !== "placeholder_zbjk5v"){
      await imageStore.deleteImage(venue.imgId);
      }
      return h.redirect("/dashboard");
    },
  },

  clearLog: {
    handler: async function (request, h) {
      await db.adminStore.deleteAlladmins();
      return h.redirect("/dashboard");
    },
  },
};
