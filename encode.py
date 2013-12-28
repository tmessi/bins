#!/bin/env python

import subprocess
import argparse


def _parseargs():
    parser = argparse.ArgumentParser(description='Encoder')
    parser.add_argument('name',
                        metavar='N',
                        type=str,
                        help='output name')
    parser.add_argument('--chapters',
                        default=None,
                        help='chapters to encode')
    parser.add_argument('--crop',
                        nargs=1,
                        default=None,
                        help='crop setting')
    parser.add_argument('--opfs',
                        type=str,
                        default='24000/1001',
                        help='opfs setting')
    parser.add_argument('--vbitrate',
                        type=int,
                        default='2400',
                        help='vbitrate setting')
    args =  parser.parse_args()
    if not args.chapters:
        args.chapters = [1]
    if args.crop:
        args.crop = ',crop={0}'.format(args.crop)
    return args


def main():
    args = _parseargs()
    passes = [1, 2]
    for chapter in args.chapters:
        for pass_ in passes:
            cmd = ['mencode',
                   'dvd://{0}'.format(chapter),
                   '-ofps', '{0}'.format(args.opfs),
                   '-oac', 'copy',
                   '-ovc', 'lavc',
                   '-lavcopts', 'vcodec=mpeg4:vbitrate={0}:v4mv:mbd=2:trell:cmp=3:subcmp=3:autoaspect:vpass={1}'.format(args.vbitrate, pass_),
                   '-vf', 'pullup,softskip{0},hqdn3d=2:1:2'.format(args.crop or ''),
                   '-mc', '0',
                   '-noskip',
                   '-ni',
                   '-o', '0}.avi'.format(args.name)]
            p = subprocess.Popen(cmd,
                                 stdout=subprocess.STDOUT)
            p.wait()


if __name__ == '__main__':
    main()
