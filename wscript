# WARNING: This wscript does not follow good practices and should not be copied
# or reproduced in your own projects.
#
#
# This file is the default set of rules to compile a Pebble application.
#
# Feel free to customize this to your needs.
#
import os.path

top = '.'
out = 'build'


def options(ctx):
    ctx.load('pebble_sdk')


def configure(ctx):
    """
    This method is used to configure your build.
    ctx.load(`pebble_sdk`) automatically configures a build for each valid
    platform in `targetPlatforms`.
    Platform-specific configuration: add your change after calling
    tx.load('pebble_sdk') and make sure to set the environment first.
    Universal configuration: add your change prior to calling
    ctx.load('pebble_sdk').
    """
    ctx.load('pebble_sdk')


def build(ctx):
    ctx.load('pebble_sdk')

    build_worker = os.path.exists('worker_src')
    binaries = []

    cached_env = ctx.env
    for platform in ctx.env.TARGET_PLATFORMS:
        ctx.env = ctx.all_envs[platform]
        ctx.set_group(ctx.env.PLATFORM_NAME)
        app_elf = '{}/pebble-app.elf'.format(ctx.env.BUILD_DIR)
        ctx.pbl_program(source=ctx.path.ant_glob('src/**/*.c'), target=app_elf)

        if build_worker:
            worker_elf = '{}/pebble-worker.elf'.format(ctx.env.BUILD_DIR)
            binaries.append({
                'platform': p,
                'app_elf': app_elf,
                'worker_elf': worker_elf
            })
            ctx.pbl_worker(source=ctx.path.ant_glob('worker_src/**/*.c'),
                           target=worker_elf)
        else:
            binaries.append({'platform': platform, 'app_elf': app_elf})
    ctx.env = cached_env

    ctx.set_group('bundle')
    # ctx(rule='../node_modules/.bin/eslint ../src/js/**/*.js',
    #     source=ctx.path.ant_glob('src/**/*.js'))
    ctx(rule='../node_modules/.bin/browserify ../src/js/app.js -o ${TGT} ' +
        '-t [ babelify --presets [ es2015 ] ]',
        source=ctx.path.ant_glob('src/**/*.js'),
        target='pebble-js-app.js')
    ctx.pbl_bundle(binaries=binaries, js='pebble-js-app.js')
