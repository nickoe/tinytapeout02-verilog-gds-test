all: update test

test:
	make -C src

update:
	#./my_litex_design.py
	docker run --rm -e LOCAL_USER_ID=`id -u ${USER}` -e LOCAL_GROUP_ID=`id -g ${USER}` -v `pwd`:/work -it nickoe-litex bash -l -c "./my_litex_design.py --trace-fst --trace --trace-end 10"
	# Hack for IO's
	sed -i 's/io_in0/io_in/g' src/user_module_nickoe.v
	sed -i 's/io_out0/io_out/g' src/user_module_nickoe.v
