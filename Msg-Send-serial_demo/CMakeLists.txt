cmake_minimum_required(VERSION 2.8.3)
project(serial_demo)
find_package(catkin REQUIRED COMPONENTS
    message_filters
	roscpp
	rospy
	std_msgs
	message_generation
	controller_manager
	gazebo_ros

	

	
	
	sensor_msgs
	geometry_msgs
	nav_msgs
	tf
	serial
	
)
## Generate messages in the 'msg' folder
add_message_files(
  FILES
  GPS.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)


catkin_package(
   #INCLUDE_DIRS include
   CATKIN_DEPENDS message_filters message_generation urdf xacro roscpp rospy std_msgs actionlib nav_msgs geometry_msgs message_runtime sensor_msgs 
)

include_directories(
#include 
${catkin_INCLUDE_DIRS} 
${PCL_INCLUDE_DIRS})


add_executable(gps_serial_tcp src/gps_serial_tcp.cpp)
add_dependencies(gps_serial_tcp ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(gps_serial_tcp
   ${catkin_LIBRARIES}
 )

add_executable(mti_710_gps src/mti_710_gps.cpp)
add_dependencies(mti_710_gps ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(mti_710_gps
   ${catkin_LIBRARIES}
 )


# add_executable(mti_710_gps_pressure src/mti_710_gps_pressure.cpp)
# add_dependencies(mti_710_gps_pressure ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
# target_link_libraries(mti_710_gps_pressure
#	${catkin_LIBRARIES}
#  )

#  add_executable(mti_710_gps_pressure_zxc src/mti_710_gps_pressure_zxc.cpp)
#  add_dependencies(mti_710_gps_pressure_zxc ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
#  target_link_libraries(mti_710_gps_pressure_zxc
#	 ${catkin_LIBRARIES}
#   )
