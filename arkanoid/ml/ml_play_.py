import arkanoid.communication as comm
from arkanoid.communication import SceneInfo, GameInstruction

def ml_loop():
	"""The main loop of the machine learning process

	This loop is run in a seperate process, and communicates with the game process.

	Note that the game process won't wait for the ml process to generate the
	GameInstrcution. It is possible that the frame of the GameInstruction
	is behind of the current frame in the game process. Try to decrease the fps
	to avoid this situation.
	"""

	# === Here is the execution order of the loop === #
	# 1. Put the initialization code here.

	# 2. Inform the game process that ml process is ready before start the loop.
	comm.ml_ready()
	pre_ball_center = (100+2.5,100+2.5)
	predes = 0
	# 3. Start an endless loop.
	while True:
		# 3.1. Receive the scene information sent from the game process.
		scene_info = comm.get_scene_info()

		# 3.2. If the game is over or passed, the game process will reset
		#      the scene immediately and send the scene information again.
		#      Therefore, receive the reset scene information.
		#      You can do proper actions, when the game is over or passed.
		if scene_info.status == SceneInfo.STATUS_GAME_OVER or \
			scene_info.status == SceneInfo.STATUS_GAME_PASS:
			scene_info = comm.get_scene_info()

		"""
			The scene_info datastructure
			self.frame = frame
			self.status = status
			self.ball = None        # tuple (x, y)
			self.platform = None    # tuple (x, y)
			self.bricks = None      # list of tuple (x, y)
		"""
		# 3.3. Put the code here to handle the scene information
		cur_ball_center = (scene_info.ball[0] + 2.5, scene_info.ball[1] + 2.5)
		cur_platform_center = (scene_info.platform[0] + 25 , scene_info.platform[1] + 2.5)

		expect_pos = cur_ball_center[0]
		if cur_ball_center[0] - pre_ball_center[0] != 0:
			# calculate the position will touch the position in line
			dir = (cur_ball_center[0] - pre_ball_center[0], cur_ball_center[1] - pre_ball_center[1])
			m = dir[1]/dir[0]
			expect_pos = (400-cur_ball_center[1])/m + cur_ball_center[0]

		while expect_pos > 200 or expect_pos < 0:
			if expect_pos > 200:
				expect_pos = 400 - expect_pos
			elif expect_pos < 0:
				expect_pos = -expect_pos

		if cur_platform_center[0] - expect_pos > 0:
			des = -1 # go left
		elif cur_ball_center[1] - pre_ball_center[1] < 0:
			des = 0
		else:
			des = 1 # go right

		if abs(predes - des) == 2:
			des = 0

		# if cur_ball_center[1] - pre_ball_center[1] < 0 or abs(cur_platform_center[0] - expect_pos) < 0.7:
		# 	des = 0
		# elif cur_platform_center[0] - expect_pos > 0:
		# 	des = -1
		# elif cur_platform_center[0] - expect_pos < 0:
		# 	des = 1
		# else:
		# 	des = 0

		# 3.4. Send the instruction for this frame to the game process
		if cur_ball_center[1] - pre_ball_center[1] != 0:
			if des > 0:
				comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
			elif des == 0:
				comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
			else:
				comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)

		predes = des
		pre_ball_center = cur_ball_center
