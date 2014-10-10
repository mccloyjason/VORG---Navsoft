// JavaScript Document

jQuery(document).ready(function(){
 
 //jQuery(".menupanl").hide()
 jQuery(".menupanl").click(function() {
 //jQuery(".pincreatropdpbox").toggle();
 jQuery(".leftmenpan").toggleClass("sleekmenuset")
 jQuery(".menupanl").toggleClass("menuactive")
 jQuery(".submenudiv").hide();
 });
 
 // left menu css 
 /*jQuery(".submenudiv").hide()
 jQuery(".asideleftlink li a").click(function() {
 jQuery(".submenudiv").toggle(500);
 jQuery(".asideleftlink li a .arrowupdown").toggleClass("arrowdown")
 });*/
 
 jQuery(".asideleftlink li").click(function() {
  jQuery(this).find(".submenudiv").toggle(500);
  //jQuery(".asideleftlink li a .arrowupdown").toggleClass("arrowdown")
 });
 
 // users dropdown css 
 jQuery(".dropdowmenu").hide()
 jQuery(".userprofill").click(function() {
 jQuery(".dropdowmenu").toggle(500);
 });
 
 jQuery('body').click(function(e) {
 if (!jQuery(e.target).closest('.avtarclass').length){
 jQuery(".dropdowmenu").hide();
 }
 if (!jQuery(e.target).closest('.settingdrop').length){
 jQuery(".settingdropdownpan").hide();
 }
 if (!jQuery(e.target).closest('.primaryorg').length){
 jQuery(".submenudiv").hide();
 }
 });
 
 // setting dropdown css 
 jQuery(".settingdropdownpan").hide()
 jQuery(".settingdrop").click(function() {
 jQuery(".settingdropdownpan").toggle(500);
 //jQuery(".asideleftlink li a .arrowupdown").toggleClass("arrowdown")
 });
 
 // mobile slider css
 jQuery(".navmobile").click(function() {
 jQuery(".leftmenpan").toggleClass("mobileleftpan");
 jQuery(".navmobile").toggleClass("navmobilactv")
 });
 
 // mobile morelinks
 jQuery(".morebsublinkdiv").hide()
 jQuery(".mobilemorelnk").click(function() {
 jQuery(".morebsublinkdiv").toggle(500);
 });
 
 
 //jQuery("#dack_menu").click(function() {
 //jQuery("#dack_sub").toggle(500);
 
 //});
 
});