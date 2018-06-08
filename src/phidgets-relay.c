/*
 * Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <phidget21.h>

static void usage(const char *appname) {
	fprintf(stderr, "usage: %s serial relay_id value\n", appname);
	exit(1);
}

static void phidgets_error(const char *func, int err) {
	int err2;
	const char* error;

	fprintf(stderr, "%s() failed:\n", func);
	err2 = CPhidget_getErrorDescription(err, &error);
	if (err != EPHIDGET_OK) {
		fprintf(stderr, "\tPCPhidget_getErrorDescription() failed: %d\n", err2);
		exit(1);
	}

	fprintf(stderr, "\t%s\n", error);
	exit(1);
}

int main(int argc, char **argv) {
	int serial, relay_id, value, err;
	CPhidgetInterfaceKitHandle ifk;

	if (argc != 4)
		usage(argv[0]);

	serial = atoi(argv[1]);
	relay_id = atoi(argv[2]);
	value = atoi(argv[3]);

	err = CPhidget_enableLogging(PHIDGET_LOG_VERBOSE, NULL);
	if (err != EPHIDGET_OK)
		phidgets_error("CPhidget_enableLogging", err);
	err = CPhidgetInterfaceKit_create(&ifk);
	if (err != EPHIDGET_OK)
		phidgets_error("CPhidgetInterfaceKit_create", err);
	err = CPhidget_open((CPhidgetHandle)ifk, serial);
	if (err != EPHIDGET_OK)
		phidgets_error("CPhidget_open", err);
	err = CPhidget_waitForAttachment((CPhidgetHandle)ifk, 0);
	if (err != EPHIDGET_OK)
		phidgets_error("CPhidget_waitForAttachment", err);
	err = CPhidgetInterfaceKit_setOutputState(ifk, relay_id, value);
	if (err != EPHIDGET_OK)
		phidgets_error("CPhidgetInterfaceKit_setOutputState", err);
	err = CPhidget_close((CPhidgetHandle)ifk);
	if (err != EPHIDGET_OK)
		phidgets_error("CPhidget_close", err);
	err = CPhidget_delete((CPhidgetHandle)ifk);
	if (err != EPHIDGET_OK)
		phidgets_error("CPhidget_delete", err);

	return 0;
}
