/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************* LICENSE ************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
//
//    Copyright © 2016 Bastien Pasdeloup (name.surname@gmail.com) and Télécom Bretagne
//
//    This file is part of PyRat.
//
//    PyRat is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    PyRat is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with PyRat.  If not, see <http://www.gnu.org/licenses/>.
//
/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************ CONSTANTS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Speed at which the dragger follows the mouse
    
    /** CODE **/
    const SPEED = 0.1;
    
/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************ FUNCTIONS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Allows a Google Maps-like way of dragging stuff
    // There must be a single element with ID mouseDraggable in the page
    
    /** CODE **/
    $(function ()
    {
        
        // Initialization
        var mouseIsDown = false;
        var originX = 0;
        var originY = 0;
        
        // We prevent drag & drop on this item
        $("#mouseDraggable").attr("onmousedown", "return false");
        
        // When mouse is moving while having button pressed, we update the view
        $(window).mousemove(function(m)
        {
            if (mouseIsDown)
            {
                $("#mouseDraggable").scrollLeft($("#mouseDraggable").scrollLeft() - SPEED * (m.pageX - originX));
                $("#mouseDraggable").scrollTop($("#mouseDraggable").scrollTop() - SPEED * (m.pageY - originY));
            }
        });

        // When mouse button becomes pressed on the draggable element, we remember the location
        $("#mouseDraggable").mousedown(function(m)
        {
            mouseIsDown = true;
            originX = m.pageX;
            originY = m.pageY;
        });

        // When mouse button becomes released anywhere, we disable dragging
        $(window).mouseup(function()
        {
            mouseIsDown = false;
        });
        
    })
    
/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/